from fastapi import APIRouter, Depends

from backend.auth import verify_admin
from backend.models import User
from backend.services import report_service

router = APIRouter(
    tags=["Reports"]
)


@router.get("/reports/employees")
def employee_report(
    admin: User = Depends(verify_admin)
):
    return report_service.employee_report()


@router.get("/reports/attendance")
def attendance_report(
    admin: User = Depends(verify_admin)
):
    return report_service.attendance_report()


@router.get("/reports/employees/csv")
def export_employee_csv(
    admin: User = Depends(verify_admin)
):
    return report_service.export_employee_csv()


@router.get("/reports/attendance/csv")
def export_attendance_csv(
    admin: User = Depends(verify_admin)
):
    return report_service.export_attendance_csv()


@router.get("/reports/leave/csv")
def export_leave_csv(
    admin: User = Depends(verify_admin)
):
    return report_service.export_leave_csv()


@router.get("/reports/payroll/csv")
def export_payroll_csv(
    admin: User = Depends(verify_admin)
):
    return report_service.export_payroll_csv()