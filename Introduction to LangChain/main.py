
import dotenv
import os
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import ToolMessage


dotenv.load_dotenv()

planets = ["earth", "jupiter", "mars", "mercury", "neptune",
                 "pluto", "saturn", "uranus", "venus"]

documents = []
for p in planets:
    loader = TextLoader(f".\\planets\\{p}.txt")
    docs = loader.load()
    documents.extend(docs)

embeddings_model = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

db = Chroma(
    collection_name="hyper-collection",
    embedding_function=embeddings_model
)

db.add_documents(documents=documents)


llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-4o-mini",  # or any OpenRouter-supported model
    temperature=0.0,
    max_retries=2
)
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an assistant that answers questions about planets. "
        "Use tools when appropriate."
    ),
    ("human", "{input}")
])


@tool("PlanetDistanceSun")
def planet_distance_sun(planet_name: str) -> str:
    """Useful to provide information about the distance between two planets."""
    if planet_name == "Earth":
        return "Earth is approximately 1 AU from the Sun."
    elif planet_name == "Mars":
        return "Mars is approximately 1.5 AU from the Sun."
    elif planet_name == "Jupiter":
        return "Jupiter is approximately 5.2 AU from the Sun."
    elif planet_name == "Pluto":
        return "Pluto is approximately 39.5 AU from the Sun."
    else:
        return f"Information about the distance of {planet_name} from the Sun is not available in this tool."

@tool("PlanetRevolutionPeriod")
def planet_revolution_period(planet_name: str) -> str:
    """Useful to provide information about the revolution period between two planets."""
    if planet_name == "Earth":
        return "Earth takes approximately 1 Earth year to revolve around the Sun."
    elif planet_name == "Mars":
        return "Mars takes approximately 1.88 Earth years to revolve around the Sun."
    elif planet_name == "Jupiter":
        return "Jupiter takes approximately 11.86 Earth years to revolve around the Sun."
    elif planet_name == "Pluto":
        return "Pluto takes approximately 248 Earth years to revolve around the Sun."
    else:
        return f"Information about the revolution period of {planet_name} is not available in this tool."


@tool("PlanetGeneralInfo")
def planet_general_info(query: str) -> str:
    """
    Use this tool for general, open-ended questions about planets
    that are NOT about distance from the Sun or revolution period.

    The input should be a natural-language search query suitable for
    semantic similarity search (e.g., "interesting facts about Jupiter",
    "composition and moons of Saturn").
    """
    extracted_doc = db.similarity_search(query, k=1)

    if not extracted_doc:
        return "Additional information is not available in this tool."

    return extracted_doc[0].page_content


tools_list = [planet_distance_sun, planet_revolution_period, planet_general_info]
model_with_tools = llm.bind_tools(tools_list)

tool_map = {
    "PlanetDistanceSun": planet_distance_sun,
    "PlanetRevolutionPeriod": planet_revolution_period,
    "PlanetGeneralInfo": planet_general_info,
}


def run_tools(ai_message):
    # If the model did not call any tools, just print the response
    if not ai_message.tool_calls:
        print(ai_message.content)
        return ai_message.content

    tool_messages = []

    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        tool_fn = tool_map[tool_name]
        tool_output = tool_fn.invoke(tool_args)

        print(tool_output)

        tool_messages.append(
            ToolMessage(
                tool_call_id=tool_call["id"],
                content=tool_output
            )
        )

    return tool_messages


tool_execution_chain = RunnableLambda(run_tools)

chain = (
        prompt
        | model_with_tools
        | tool_execution_chain
)

user_query = input("> ")

chain.invoke({"input": user_query})
print()
print(chain)

