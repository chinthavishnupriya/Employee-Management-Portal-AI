import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.ai.resume_ai import resume_ai
from backend.ai.semantic_search import semantic_search

router = APIRouter(
    prefix="/resume",
    tags=["Resume AI"]
)


class SearchRequest(BaseModel):
    query: str


UPLOAD_FOLDER = "backend/resume_storage/resumes"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    analysis = resume_ai.analyze_resume(file_path)

    return {
        "filename": file.filename,
        "analysis": analysis
    }


@router.post("/search")
def search_resume(request: SearchRequest):

    results = semantic_search.search(
        query=request.query,
        top_k=5
    )

    return {
        "results": results
    }