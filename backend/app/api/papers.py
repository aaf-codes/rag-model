from fastapi import APIRouter
import os

from app.services.vectordb_service import (
    list_all_papers,
    delete_paper
)

router = APIRouter()

# Upload folder path
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "uploads"
)

# List all uploaded papers
@router.get("/papers")
def get_papers():

    papers = list_all_papers()

    return {
        "papers": papers
    }


# Delete paper
@router.delete("/delete-paper/{filename}")
def remove_paper(filename: str):

    # Delete from ChromaDB
    deleted_ids = delete_paper(filename)

    # Delete physical PDF file
    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    return {
        "message": "Paper deleted successfully",
        "deleted_chunks": len(deleted_ids)
    }