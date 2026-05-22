import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="research_papers"
)

# Store embeddings in ChromaDB
def store_embedding(chunk, embedding, filename, chunk_index):

    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        ids=[f"{filename}_{chunk_index}"],
        metadatas=[{
            "paper": filename,
            "chunk_index": chunk_index
        }]
    )

# Search similar chunks
def search_similar_chunks(query_embedding):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    return results

# List all uploaded papers
def list_all_papers():

    results = collection.get()

    papers = set()

    for metadata in results["metadatas"]:
        papers.add(metadata["paper"])

    return list(papers)

# Delete paper from database
def delete_paper(filename):

    results = collection.get()

    ids_to_delete = []

    for index, metadata in enumerate(results["metadatas"]):

        if metadata["paper"] == filename:
            ids_to_delete.append(results["ids"][index])

    if ids_to_delete:
        collection.delete(ids=ids_to_delete)

    return ids_to_delete