import os
import shutil

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from backend.rag.rag_service import rag_service


router = APIRouter(
    prefix="/rag",
    tags=["RAG HR Policy"]
)


UPLOAD_FOLDER = "backend/rag/policies"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ChatRequest(BaseModel):
    question: str


@router.post("/upload-policy")
async def upload_policy(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = rag_service.ingest_pdf(file_path)

    return {
        "message": "Policy uploaded successfully.",
        "chunks": chunks
    }


@router.post("/chat")
def chat(request: ChatRequest):

    answer = rag_service.ask(request.question)

    return {
        "answer": answer
    }