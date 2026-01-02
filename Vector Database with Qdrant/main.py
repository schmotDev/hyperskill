import dotenv
import os
os.environ["USER_AGENT"] = "Mozilla/5.0 (compatible; MovieScraper/1.0)"

from langchain_community.document_loaders import IMSDbLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import requests
import re
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


dotenv.load_dotenv()
api_key=os.environ.get("OPENROUTER_API_KEY", None)

url_all_movies = "https://imsdb.com/all-scripts.html"
response = requests.get(url_all_movies)

soup = BeautifulSoup(response.text, "html.parser")

movie_names = [a.get_text(strip=True) for a in soup.select("p a")]

for i, title in enumerate(movie_names, start=1):
    print(f"{i}. {title}")
print()

user_input = input("> ")
if user_input in movie_names:
    title = user_input.replace(" ", "-")
    url_movie = f"https://imsdb.com/scripts/{title}.html"
    loader = IMSDbLoader(url_movie)
    data = loader.load()
    text = data[0].page_content
    text = re.sub(r'\s+', ' ', text).strip()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=10,
        separators=["INT."],
        keep_separator="start"  # ensures "INT." stays at start of chunk
    )

    scene_chunks = splitter.split_text(text)



    print(f"Loaded script for {user_input} from {url_movie}.")
    print()

    print(f"Found {len(scene_chunks)} scenes in the script for {user_input}.\n")
    #for i, scene in enumerate(scene_chunks, start=1):
    #    print(f"Scene {i}: {scene.strip()}")

    collection_name = title
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # 384 dimensions
    qdrant_client = QdrantClient(
        url="http://192.168.50.68:6333"  # Qdrant REST API endpoint
    )
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    vector_store = QdrantVectorStore.from_texts(
        texts=scene_chunks,
        embedding=embeddings_model,
        collection_name=collection_name,
        url="http://192.168.50.68:6333",
    )
    print(f'Embedded script for {user_input}.')


    print()
    user_query = input("> ")

    llm = ChatOpenAI(
        model="openai/gpt-4o-mini",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2
    )

    rewrite_prompt = ChatPromptTemplate.from_messages([
        ("system", """
    You are a query rewriter for a movie scene retrieval system.
    
    The system retrieves scenes based on semantic similarity to scene descriptions.
    
    Rewrite the user's query so that it:
    - ensures that it emphasizes the necessary keywords for scene retrieval
    - Uses clear, descriptive language
    - Avoids questions or conversational phrasing
    - Is optimized for embedding-based retrieval
    
    Return ONLY the rewritten query.
    
    example:
    users' query: "Only scenes involving trains"
    Your rewritten query: "Find scenes featuring trains."
    """),
        ("human", "{query}")
    ])

    query_rewriter = rewrite_prompt | llm | StrOutputParser()

    rewritten_query = query_rewriter.invoke({
        "query": user_query
    })

    print(f"Rewritten query to: \"{rewritten_query}\"")
    print()

    results = vector_store.similarity_search(
        rewritten_query,
        k=5
    )

    #for i, doc in enumerate(results, start=1):
    #    print(f"Scene {i}: {doc.page_content}")

    context_text = "\n\n---\n\n".join(
        doc.page_content for doc in results
    )

    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", """
    You are an expert screenwriter and movie script analyst.

    You are given:
    - A user request
    - Relevant context extracted from movie script scenes

    Your task:
    - Use ONLY the provided context when appropriate
    - Expand, adapt, or creatively synthesize scenes if requested
    - Write in proper screenplay format when applicable
    - Be vivid, descriptive, and faithful to cinematic conventions

    If the user asks to create or rewrite a scene, respond in screenplay format.
    """),
        ("human", """
    USER REQUEST:
    {query}

    RELEVANT SCRIPT CONTEXT:
    {context}

    Write a detailed and insightful response.
    """)
    ])

    answer_chain = answer_prompt | llm | StrOutputParser()

    final_answer = answer_chain.invoke({
        "query": user_query,
        "context": context_text
    })

    print("Final Answer:")
    print(final_answer)


else:
    print(f"Script for '{user_input}' wasn't found in the list of movie scripts.")

