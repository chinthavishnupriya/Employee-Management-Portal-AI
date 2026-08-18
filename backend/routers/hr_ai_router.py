from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import SessionLocal
from backend.models import User, Employee
from backend.ai.ai_service import ai_service


router = APIRouter(
    prefix="/hr-ai",
    tags=["HR AI"]
)


class HRQuestion(BaseModel):
    question: str


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/ask")
def ask_ai(
    data: HRQuestion,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    print("=" * 60)
    print("HR AI REQUEST")
    print("USER:", current_user.email)
    print("ROLE:", current_user.role)
    print("QUESTION:", data.question)

    employee = (
        db.query(Employee)
        .filter(
            Employee.email.ilike(current_user.email.strip())
        )
        .first()
    )

    if employee is None:

        print(
            "NO EMPLOYEE MATCH FOR:",
            current_user.email
        )

        return {
            "role": current_user.role,
            "answer": (
                "Employee profile not found. "
                "Your login account is not linked to an employee record."
            )
        }

    print(
        "EMPLOYEE FOUND:",
        employee.id,
        employee.full_name,
        employee.email
    )

    answer = ai_service.ask(
        prompt=data.question,
        db=db,
        employee_id=employee.id
    )

    print("AI ANSWER:", answer)

    return {
        "role": current_user.role,
        "answer": answer
    }
