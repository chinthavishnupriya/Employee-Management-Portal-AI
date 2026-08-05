from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Department
from datetime import date

from backend.models import (
    User,
    Attendance,
    LeaveRequest,
    Payroll,
    Performance
)
from backend.models.employee import Employee

def create_department(department):

    db: Session = SessionLocal()

    try:

        new_department = Department(
            department_name=department.department_name,
            description=department.description
        )

        db.add(new_department)
        db.commit()
        db.refresh(new_department)

        return {
            "message": "Department created successfully",
            "department": new_department
        }

    except Exception as e:
        db.rollback()

        return {
            "error": str(e)
        }

    finally:
        db.close()


def get_departments():

    db: Session = SessionLocal()

    try:

        departments = db.query(Department).all()

        return departments

    finally:
        db.close()

def employee_dashboard(current_user):

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
                "message": "Employee not found"
            }

        attendance_count = db.query(Attendance).filter(
            Attendance.employee_id == employee.id
        ).count()

        leave_count = db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee.id
        ).count()

        payroll_count = db.query(Payroll).filter(
            Payroll.employee_id == employee.id
        ).count()

        performance_count = db.query(Performance).filter(
            Performance.employee_id == employee.id
        ).count()

        today = db.query(Attendance).filter(
            Attendance.employee_id == employee.id,
            Attendance.attendance_date == date.today()
        ).first()

        return {

            "employee": {

                "employee_id": employee.employee_id,
                "full_name": employee.full_name,
                "designation": employee.designation,
                "department": employee.department.department_name

            },

            "attendance_count": attendance_count,

            "leave_count": leave_count,

            "payroll_count": payroll_count,

            "performance_count": performance_count,

            "today_attendance": {

                "status": today.status if today else "Not Checked In",
                "check_in": str(today.check_in) if today else "-",
                "check_out": str(today.check_out) if today else "-"

            }

        }

    finally:

        db.close()