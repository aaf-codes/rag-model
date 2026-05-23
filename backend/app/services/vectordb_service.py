import chromadb


# RELEVANCE THRESHOLD
# Smaller distance = more relevant
RELEVANCE_THRESHOLD = 0.7


# PERSISTENT CHROMADB CLIENT
client = chromadb.PersistentClient(
    path="chroma_db"
)


# CREATE COLLECTION
collection = client.get_or_create_collection(
    name="research_papers"
)


# STORE EMBEDDINGS
def store_embedding(
    chunk,
    embedding,
    filename,
    chunk_index,
    title,
    authors,
    year,
    section
):

    collection.add(

        documents=[chunk],

        embeddings=[embedding],

        ids=[
            f"{filename}_{chunk_index}"
        ],

        metadatas=[{

            "paper":
            filename,

            "chunk_index":
            chunk_index,

            "title":
            title,

            "authors":
            authors,

            "year":
            year,

            "section":
            section

        }]
    )


# SEARCH SIMILAR CHUNKS
def search_similar_chunks(
    query_embedding
):

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=5,

        include=[

            "documents",

            "metadatas",

            "distances"

        ]
    )

    return results


# LIST ALL PAPERS
def list_all_papers():

    results = collection.get()

    papers = []

    seen_titles = set()

    if results["metadatas"]:

        for metadata in results["metadatas"]:

            if metadata:

                title = metadata.get(
                    "title",
                    "Unknown Title"
                )

                # AVOID DUPLICATES
                if title not in seen_titles:

                    papers.append({

                        "title":
                        title,

                        "authors":
                        metadata.get(
                            "authors",
                            "Unknown Author"
                        ),

                        "year":
                        metadata.get(
                            "year",
                            "Unknown Year"
                        ),

                        "paper":
                        metadata.get(
                            "paper"
                        )

                    })

                    seen_titles.add(title)

    return papers


# DELETE PAPER
def delete_paper(filename):

    results = collection.get()

    ids_to_delete = []

    if results["metadatas"]:

        for index, metadata in enumerate(
            results["metadatas"]
        ):

            if (
                metadata and
                metadata.get("paper") == filename
            ):

                ids_to_delete.append(
                    results["ids"][index]
                )

    # DELETE FROM CHROMADB
    if ids_to_delete:

        collection.delete(
            ids=ids_to_delete
        )

    return ids_to_delete


# CHECK IF PAPER ALREADY EXISTS
def paper_exists(filename):

    results = collection.get()

    if results["metadatas"]:

        for metadata in results["metadatas"]:

            if (
                metadata and
                metadata.get("paper") == filename
            ):

                return True

    return False