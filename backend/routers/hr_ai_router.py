from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.auth import get_current_user
from backend.services.hr_ai_service import ask_hr_ai

router = APIRouter(
    prefix="/hr-ai",
    tags=["HR AI"]
)


class HRQuestion(BaseModel):
    question: str


@router.post("/ask")
def ask_ai(
    data: HRQuestion,
    current_user=Depends(get_current_user)
):

    print("=" * 50)
    print("QUESTION:", data.question)

    answer = ask_hr_ai(
        question=data.question,
        role=current_user.role,
        email=current_user.email
)

    print("AI ANSWER:", answer)
    return {
        "role": current_user.role,
        "answer": answer
    }