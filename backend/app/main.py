from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.query import router as query_router
from app.api.papers import router as papers_router

app = FastAPI(
    title="RAG Research Citation Assistant",
    version="1.0.0"
)

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "RAG Research Assistant API Running"
    }

# ROUTERS
app.include_router(upload_router)
app.include_router(query_router)
app.include_router(papers_router)