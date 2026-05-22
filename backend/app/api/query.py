from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import create_embedding
from app.services.vectordb_service import search_similar_chunks
from app.services.generation_service import generate_related_work

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def query_papers(data: QueryRequest):

    # Convert query into embedding
    query_embedding = create_embedding(data.query)

    # Retrieve relevant chunks
    results = search_similar_chunks(query_embedding)

    retrieved_chunks = results["documents"][0]

    # Source papers
    source_papers = []

    for metadata in results["metadatas"][0]:
        source_papers.append(metadata["paper"])

    # Remove duplicates
    source_papers = list(set(source_papers))

    # Generate AI summary
    summary = generate_related_work(
        data.query,
        retrieved_chunks
    )

    return {
        "summary": summary,
        "retrieved_chunks": retrieved_chunks,
        "source_papers": source_papers
    }