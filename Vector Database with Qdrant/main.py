from qdrant_client.http.models.models import ScoredPoint
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
from openai import OpenAI
import re
from qdrant_client.http import models
from fastapi import FastAPI
from typing import Optional, List, Dict
from pydantic import BaseModel

COLLECTION_NAME = "arxiv_papers"

load_dotenv()
api_key=os.environ.get("OPENROUTER_API_KEY", None)
#api_key=os.environ.get("OPENAI_API_KEY", None)

url_api="https://openrouter.ai/api/v1"
#url_api = "https://api.openai.com/v1"

openai_client = OpenAI(
    api_key=api_key,
    base_url=url_api
)

app = FastAPI()


class SearchRequest(BaseModel):
    """
    Model representing a search request sent by a client.
    """
    query: str
    top_n: Optional[int] = 5


class SearchResult(BaseModel):
    """
    Model representing an individual search result.
    """
    id: str
    payload: Dict
    score: float


class SearchResponse(BaseModel):
    """
    Model representing the response returned to a client after a search.
    """
    results: List[SearchResult]


def extract_author_name(query: str) -> Optional[str]:
    pattern = r"by\s+([A-Za-z\s\-]+)"
    match = re.search(pattern, query, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None


def search_similar_with_optional_author(
    collection_name: str,
    query_vector: list[float],
    author_name: Optional[str] = None,
    top_k: int = 3
    ) -> List[ScoredPoint]:

    client = QdrantClient(host="localhost", port=6333, timeout=120)

    if author_name is not None:
        search_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="authors",
                    match=models.MatchText(text=author_name),
                )
            ]
        )

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        with_vectors=False,
        query_filter=search_filter,
    ).points

    return results


def embed_query(query: str) -> list[float]:
    cleaned_query = query.replace("\n", " ")

    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=cleaned_query,
    )

    return response.data[0].embedding


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    # 1. Extract author (optional)
    author_name = extract_author_name(request.query)

    # 2. Embed the query
    query_embedding = embed_query(request.query)

    # 3. Run vector search with optional author filter
    results = search_similar_with_optional_author(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        author_name=author_name,
        top_k=request.top_n,
    )

    # 4. Format results
    formatted_results = []

    for point in results:
        formatted_results.append(
            SearchResult(
                id=point.payload["id"],
                payload=point.payload,
                score=point.score,
            )
        )

    # 5. Return response
    return SearchResponse(results=formatted_results)
