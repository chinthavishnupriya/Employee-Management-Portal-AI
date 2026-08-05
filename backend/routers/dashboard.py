from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import (
    User,
    Employee,
    Department,
    Attendance,
    LeaveRequest,
    Payroll,
    Performance,
    EmployeeDocument,
    Onboarding,
    Offboarding
)
from backend.auth import verify_token

router = APIRouter(
    tags=["Dashboard"]
)


@router.get("/dashboard")
def dashboard(
    current_user: str = Depends(verify_token)
):
    db: Session = SessionLocal()

    try:
        total_users = db.query(User).count()
        total_employees = db.query(Employee).count()
        total_departments = db.query(Department).count()
        total_attendance = db.query(Attendance).count()

        return {
            "total_users": total_users,
            "total_employees": total_employees,
            "total_departments": total_departments,
            "total_attendance": total_attendance
        }

    finally:
        db.close()


@router.get("/dashboard/analytics")
def dashboard_analytics(
    current_user: str = Depends(verify_token)
):
    db: Session = SessionLocal()

    try:
        total_users = db.query(User).count()
        total_employees = db.query(Employee).count()
        total_departments = db.query(Department).count()
        total_attendance = db.query(Attendance).count()
        total_leave_requests = db.query(LeaveRequest).count()

        approved_leaves = db.query(LeaveRequest).filter(
            LeaveRequest.status == "Approved"
        ).count()

        rejected_leaves = db.query(LeaveRequest).filter(
            LeaveRequest.status == "Rejected"
        ).count()

        pending_leaves = db.query(LeaveRequest).filter(
            LeaveRequest.status == "Pending"
        ).count()

        payroll_records = db.query(Payroll).all()
        total_performance = db.query(Performance).count()
        total_documents = db.query(EmployeeDocument).count()
        total_onboarding = db.query(Onboarding).count()
        total_offboarding = db.query(Offboarding).count()
        total_salary_paid = sum(
            payroll.net_salary for payroll in payroll_records
        )

        return {
            "total_users": total_users,
            "total_employees": total_employees,
            "total_departments": total_departments,
            "total_attendance": total_attendance,
            "total_leave_requests": total_leave_requests,
            "approved_leaves": approved_leaves,
            "rejected_leaves": rejected_leaves,
            "pending_leaves": pending_leaves,
            "total_payroll_records": len(payroll_records),
            "total_salary_paid": total_salary_paid,
            "total_performance": total_performance,
            "total_documents": total_documents,
            "total_onboarding": total_onboarding,
            "total_offboarding": total_offboarding
        }

    finally:
        db.close()