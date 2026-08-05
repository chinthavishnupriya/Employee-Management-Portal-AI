from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.auth import verify_token
from backend.models import User, Employee

router = APIRouter(
    tags=["Current User"]
)


@router.get("/me")
def get_me(
    current_user: str = Depends(verify_token)
):
    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == current_user
        ).first()

        if user is None:
            return {
                "message": "User not found"
            }

        employee = db.query(Employee).filter(
            Employee.email == user.email
        ).first()

        if employee is None:

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,

            "employee_id": employee.employee_id,
            "full_name": employee.full_name,
            "department_id": employee.department_id,
            "designation": employee.designation,
            "salary": employee.salary
        }

    finally:
        db.close()