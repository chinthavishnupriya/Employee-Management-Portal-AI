from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Employee, employee
from backend.routers import profile


def get_profile(current_user):

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

            "emergency_contact": employee.emergency_contact,

            "date_of_birth": employee.date_of_birth,

            "joining_date": employee.joining_date,

            "nationality": employee.nationality,

            "profile_photo": employee.profile_photo


        }

    finally:

        db.close()


def update_profile(current_user, profile):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.email == current_user
        ).first()

        if employee is None:

            return {
                "message": "Employee not found"
            }

        employee.phone = profile.phone

        employee.address = profile.address

        employee.emergency_contact = profile.emergency_contact

        employee.date_of_birth = profile.date_of_birth

        employee.joining_date = profile.joining_date

        employee.nationality = profile.nationality

        employee.profile_photo = profile.profile_photo

        db.commit()

        db.refresh(employee)

        return {

            "message": "Profile updated successfully",

            "employee": employee

        }

    finally:

        db.close()