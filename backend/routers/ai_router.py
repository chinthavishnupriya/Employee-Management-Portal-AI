from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.ai.ai_service import ai_service
from backend.auth import get_current_user
from backend.database import SessionLocal
from backend.models import User, Employee

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)


class ChatRequest(BaseModel):
    prompt: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    employee = (
        db.query(Employee)
        .filter(Employee.email == current_user.email)
        .first()
    )

    if employee is None:
        return {
            "response": "Employee profile not found."
        }

    response = ai_service.ask(
        prompt=request.prompt,
        db=db,
        employee_id=employee.id
    )

    return {
        "response": response
    }