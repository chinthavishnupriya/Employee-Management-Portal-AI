from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Employee


def get_employee_details(current_user):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.email == current_user
        ).first()

        if employee is None:
            return {
                "message": "Employee not found"
            }

        return {

            "employee_id": employee.employee_id,
            "full_name": employee.full_name,
            "email": employee.email,
            "department": employee.department.department_name,
            "designation": employee.designation,
            "salary": employee.salary,
            "phone": employee.phone,
            "address": employee.address,
            "joining_date": employee.joining_date,
            "date_of_birth": employee.date_of_birth,
            "nationality": employee.nationality,
            "emergency_contact": employee.emergency_contact,
            "profile_photo": employee.profile_photo

        }

    finally:

        db.close()