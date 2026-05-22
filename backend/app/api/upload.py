from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import split_text_into_chunks
from app.services.embedding_service import create_embedding
from app.services.vectordb_service import store_embedding

router = APIRouter()

# Upload folder path
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "uploads"
)

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload-paper")
async def upload_paper(file: UploadFile = File(...)):

    try:

        # Validate PDF
        if not file.filename.endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        # Full file path
        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        # Save uploaded PDF
        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(
            file_path
        )

        # Empty PDF check
        if not extracted_text.strip():

            raise HTTPException(
                status_code=400,
                detail="No text found inside PDF"
            )

        # Split into chunks
        chunks = split_text_into_chunks(
            extracted_text
        )

        # Create embeddings + store
        for index, chunk in enumerate(chunks):

            embedding = create_embedding(chunk)

            store_embedding(
                chunk=chunk,
                embedding=embedding,
                filename=file.filename,
                chunk_index=index
            )

        return {
            "message": "PDF uploaded successfully ✅",
            "filename": file.filename,
            "total_chunks": len(chunks)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )