from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import (
    create_embedding
)

from app.services.vectordb_service import (
    search_similar_chunks,
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

    # SEARCH SIMILAR CHUNKS
    results = search_similar_chunks(
        query_embedding
    )

    # EXTRACT RESULTS
    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]

    # FILTER RELEVANT CHUNKS
    filtered_chunks = []

    source_papers = set()

    for doc, metadata, distance in zip(

        documents,
        metadatas,
        distances

    ):

        # KEEP ONLY RELEVANT CHUNKS
        if distance <= RELEVANCE_THRESHOLD:

            filtered_chunks.append({

                "text":
                doc,

                "section":
                metadata.get(
                    "section",
                    "Unknown Section"
                )

            })

            source_papers.add(
                metadata["paper"]
            )

    # NO RELEVANT RESULTS
    if len(filtered_chunks) == 0:

        return {

            "summary":
            "No sufficiently relevant papers were found in your library for this query",

            "retrieved_chunks":
            [],

            "source_papers":
            []

        }

    # SECTION-AWARE CONTEXT
    chunk_texts = []

    for chunk in filtered_chunks:

        chunk_texts.append(

            f"[{chunk['section']}]\n{chunk['text']}"

        )

    # GENERATE AI SUMMARY
    summary = generate_related_work(

        data.query,

        chunk_texts

    )

    return {

        "summary":
        summary,

        "retrieved_chunks":
        chunk_texts,

        "source_papers":
        list(source_papers)

    }