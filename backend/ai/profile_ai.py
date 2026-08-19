from sqlalchemy.orm import Session

from backend.models.employee import Employee


class ProfileAI:

    def get_profile_by_name(self, db: Session, name: str):
        employee = (
            db.query(Employee)
            .filter(Employee.full_name.ilike(f"%{name}%"))
            .first()
        )

        if employee is None:
            return None

        department = (
            employee.department.department_name
            if employee.department
            else "Not Assigned"
        )

        return {
            "employee_id": employee.employee_id,
            "full_name": employee.full_name,
            "email": employee.email,
            "phone": employee.phone,
            "address": employee.address,
            "emergency_contact": employee.emergency_contact,
            "designation": employee.designation,
            "department": department,
            "salary": employee.salary,
            "joining_date": str(employee.joining_date),
            "date_of_birth": str(employee.date_of_birth),
            "nationality": employee.nationality
        }

    def get_profile(self, db: Session, employee_id: int):

        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if employee is None:
            return None

        department = (
            employee.department.department_name
            if employee.department
            else "Not Assigned"
        )

        return {
            "employee_id": employee.employee_id,
            "full_name": employee.full_name,
            "email": employee.email,
            "phone": employee.phone,
            "address": employee.address,
            "emergency_contact": employee.emergency_contact,
            "designation": employee.designation,
            "department": department,
            "salary": employee.salary,
            "joining_date": str(employee.joining_date),
            "date_of_birth": str(employee.date_of_birth),
            "nationality": employee.nationality
        }


profile_ai = ProfileAI()