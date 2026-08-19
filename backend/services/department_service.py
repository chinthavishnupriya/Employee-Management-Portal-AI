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

# ==========================
# Update Department
# ==========================
def update_department(department_id, department):

    db: Session = SessionLocal()

    try:

        existing = db.query(Department).filter(
            Department.id == department_id
        ).first()

        if existing is None:
            return {
                "error": "Department not found"
            }

        existing.department_name = department.department_name
        existing.description = department.description

        db.commit()
        db.refresh(existing)

        return {
            "message": "Department updated successfully",
            "department": existing
        }

    except Exception as e:

        db.rollback()

        return {
            "error": str(e)
        }

    finally:

        db.close()


# ==========================
# Delete Department
# ==========================
def delete_department(department_id):

    db: Session = SessionLocal()

    try:

        existing = db.query(Department).filter(
            Department.id == department_id
        ).first()

        if existing is None:
            return {
                "error": "Department not found"
            }

        # Do not delete a department that still has employees.
        employee_count = db.query(Employee).filter(
            Employee.department_id == department_id
        ).count()

        if employee_count > 0:
            return {
                "error": "Cannot delete department because employees are assigned to it."
            }

        db.delete(existing)
        db.commit()

        return {
            "message": "Department deleted successfully"
        }

    except Exception as e:

        db.rollback()

        return {
            "error": str(e)
        }

    finally:

        db.close()
