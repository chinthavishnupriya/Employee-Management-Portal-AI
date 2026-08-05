from fastapi import APIRouter, Depends
from backend.auth import verify_token
from backend.schemas import AttendanceCreate
from backend.auth import verify_token, verify_admin
from backend.services import attendance_service

router = APIRouter(
    tags=["Attendance"]
)


@router.post("/attendance/check-in")
def check_in(
    current_user: str = Depends(verify_token)
):
    print("================================")
    print("CURRENT USER:", current_user)
    print("TYPE:", type(current_user))
    print("================================")

    return attendance_service.check_in(current_user)


@router.put("/attendance/check-out")
def check_out(
    current_user: str = Depends(verify_token)
):
    return attendance_service.check_out(current_user)
@router.get("/attendance/me")
def my_attendance(
    current_user: str = Depends(verify_token)
):
    return attendance_service.my_attendance(current_user)
@router.get("/attendance/my-summary")
def my_summary(
    current_user: str = Depends(verify_token)
):
    return attendance_service.my_summary(current_user)
@router.get("/attendance/analytics")
def attendance_analytics(
    current_user: str = Depends(verify_token)
):
    return attendance_service.attendance_analytics()
@router.get("/attendance")
def get_all_attendance(
    current_user: str = Depends(verify_token)
):
    return attendance_service.get_all_attendance()

@router.put("/attendance/{attendance_id}")
def update_attendance(
    attendance_id: int,
    check_in: str,
    check_out: str,
    admin=Depends(verify_admin)
):
    return attendance_service.update_attendance(
        attendance_id,
        check_in,
        check_out
    )
@router.get("/attendance/{employee_id}")
def get_employee_attendance(
    employee_id: int,
    current_user: str = Depends(verify_token)
):
    return attendance_service.get_employee_attendance(employee_id)

