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

    print("=" * 60)
    print("AI CHAT REQUEST")
    print("ROLE:", current_user.role)
    print("EMAIL:", current_user.email)
    print("QUESTION:", request.prompt)

    prompt_lower = request.prompt.lower().strip()

    # ==========================================================
    # EMPLOYEE SECURITY
    # Employees can access ONLY their own information.
    # ==========================================================

    if current_user.role == "Employee":

        restricted_phrases = [
            "show all employees",
            "show all employee",
            "list all employees",
            "list employees",
            "employee list",
            "all employees",
            "all employee",
            "employees list",
            "show employees",
            "show employee list",
            "all employee details",
            "employee details",
            "other employees",
            "other employee",
            "employees information",
            "employee information",
            "employees data",
            "employee data",
            "all salaries",
            "salary of employees",
            "salary of other",
            "payroll of employees",
            "attendance of employees",
            "leave of employees",
            "performance of employees"
        ]

        for phrase in restricted_phrases:

            if phrase in prompt_lower:

                print("EMPLOYEE ACCESS BLOCKED:", phrase)

                return {
                    "response":
                    "Sorry, you are not authorized to access other employees' information."
                }

    # ==========================================================
    # ADMIN AI
    # ==========================================================
    # Admin users do not need an Employee record.
    # They must be allowed to reach AIService so that
    # database-wide queries such as "show all employees"
    # can be processed.

    if current_user.role != "Employee":

        print("ADMIN AI REQUEST")

        response = ai_service.ask(
            prompt=request.prompt,
            db=db,
            employee_id=None
        )

        print("AI RESPONSE:", response)

        return {
            "response": response
        }

    # ==========================================================
    # FIND LOGGED-IN EMPLOYEE
    # ==========================================================

    employee = (
        db.query(Employee)
        .filter(
            Employee.email == current_user.email
        )
        .first()
    )

    if employee is None:

        print("EMPLOYEE PROFILE NOT FOUND")

        return {
            "response": "Employee profile not found."
        }

    print("EMPLOYEE ID:", employee.id)
    print("EMPLOYEE NAME:", employee.full_name)

    # ==========================================================
    # SEND EMPLOYEE REQUEST TO AI SERVICE
    # ==========================================================

    response = ai_service.ask(
        prompt=request.prompt,
        db=db,
        employee_id=employee.id
    )

    print("AI RESPONSE:", response)

    return {
        "response": response
    }
