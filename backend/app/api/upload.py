from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

import os
import shutil

from app.services.pdf_service import (
    extract_text_from_pdf,
    extract_paper_metadata
)

from app.services.chunk_service import (
    split_text_into_chunks
)

from app.services.embedding_service import (
    create_embedding
)

from app.services.vectordb_service import (
    store_embedding,
    paper_exists
)

router = APIRouter()


# UPLOAD FOLDER PATH
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    ),
    "uploads"
)


# CREATE UPLOADS FOLDER
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@router.post("/upload-paper")
async def upload_paper(
    file: UploadFile = File(...)
):

    try:

        # VALIDATE PDF
        if not file.filename.endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        # CHECK DUPLICATE PAPER
        if paper_exists(file.filename):

            raise HTTPException(

                status_code=409,

                detail=
                "This paper has already been uploaded. Delete it first if you want to re-index it."

            )

        # FILE PATH
        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        # SAVE PDF
        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # EXTRACT FULL TEXT
        extracted_text = extract_text_from_pdf(
            file_path
        )

        # EXTRACT PAPER METADATA
        metadata = extract_paper_metadata(
            file_path
        )

        # EMPTY PDF CHECK
        if not extracted_text.strip():

            raise HTTPException(
                status_code=400,
                detail="No text found inside PDF"
            )

        # SECTION-AWARE CHUNKING
        chunks = split_text_into_chunks(
            extracted_text
        )

        # LIMIT CHUNKS
        chunks = chunks[:5]

        # CREATE EMBEDDINGS + STORE
        for index, chunk_data in enumerate(chunks):

            chunk_text = (
                chunk_data["text"]
            )

            section_name = (
                chunk_data["section"]
            )

            embedding = create_embedding(
                chunk_text
            )

            store_embedding(

                chunk=chunk_text,

                embedding=embedding,

                filename=file.filename,

                chunk_index=index,

                title=metadata["title"],

                authors=metadata["authors"],

                year=metadata["year"],

                section=section_name

            )

        return {

            "message":
            "PDF uploaded successfully ✅",

            "filename":
            file.filename,

            "title":
            metadata["title"],

            "authors":
            metadata["authors"],

            "year":
            metadata["year"],

            "stored_chunks":
            len(chunks)

        }

    except HTTPException as e:

        raise e

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )