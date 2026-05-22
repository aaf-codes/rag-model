from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text_into_chunks(text):

    # Bigger chunk size
    # = fewer embeddings
    # = faster uploads

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=1200,

        chunk_overlap=100,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )

    chunks = text_splitter.split_text(text)

    # Remove tiny useless chunks
    cleaned_chunks = []

    for chunk in chunks:

        if len(chunk.strip()) > 100:

            cleaned_chunks.append(chunk)

    return cleaned_chunks