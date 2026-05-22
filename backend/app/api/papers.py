from fastapi import APIRouter

from app.services.vectordb_service import (
    list_all_papers,
    delete_paper
)

router = APIRouter()

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

    deleted_ids = delete_paper(filename)

    return {
        "message": "Paper deleted successfully",
        "deleted_chunks": len(deleted_ids)
    }