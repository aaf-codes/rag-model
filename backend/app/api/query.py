from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import (
    create_embedding
)

# UPDATED: Import query_embeddings instead of search_similar_chunks
from app.services.vectordb_service import (
    query_embeddings,
    RELEVANCE_THRESHOLD
)

from app.services.generation_service import (
    generate_related_work
)

router = APIRouter()


# REQUEST MODEL
class QueryRequest(BaseModel):
    query: str


@router.post("/query")
def query_papers(data: QueryRequest):

    # CONVERT QUERY TO EMBEDDING
    query_embedding = create_embedding(
        data.query
    )

    # UPDATED: SEARCH SIMILAR CHUNKS USING NEW PIPELINE
    results = query_embeddings(
        query_embedding
    )

    # EXTRACT RESULTS (Removed [0] because the new database service handles it)
    documents = results["documents"]
    metadatas = results["metadatas"]
    distances = results["distances"]

    # FILTER RELEVANT CHUNKS
    filtered_chunks = []
    filtered_metadatas = []  # Added to track metadata for passing score papers
    source_papers = set()

    for doc, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        # KEEP ONLY RELEVANT CHUNKS
        if distance <= RELEVANCE_THRESHOLD:
            filtered_chunks.append({
                "text": doc,
                "section": metadata.get(
                    "section",
                    "Unknown Section"
                )
            })
            
            # Save metadata for matching relevant chunks
            filtered_metadatas.append(metadata)

            source_papers.add(
                metadata["paper"]
            )

    # NO RELEVANT RESULTS
    if len(filtered_chunks) == 0:
        return {
            "summary": "No sufficiently relevant papers were found in your library for this query",
            "retrieved_chunks": [],
            "source_papers": []
        }

    # SECTION-AWARE CONTEXT
    chunk_texts = []
    for chunk in filtered_chunks:
        chunk_texts.append(
            f"[{chunk['section']}]\n{chunk['text']}"
        )

    # NEW: TRAINER'S CITATION PIPELINE WIRING
    # Build a deduplicated list of paper references from retrieved chunk metadata
    paper_refs = {}
    for meta in filtered_metadatas:
        paper_key = meta.get("paper")
        
        if paper_key not in paper_refs:
            paper_refs[paper_key] = {
                "title": meta.get("title", paper_key),
                "authors": meta.get("authors", "Unknown"),
                "year": meta.get("year", "n.d."),
            }

    # UPDATED: GENERATE AI SUMMARY WITH EXTRA REFERENCE DATA
    summary = generate_related_work(
        chunk_texts, 
        list(paper_refs.values())
    )

    return {
        "summary": summary,
        "retrieved_chunks": chunk_texts,
        "source_papers": list(source_papers)
    }