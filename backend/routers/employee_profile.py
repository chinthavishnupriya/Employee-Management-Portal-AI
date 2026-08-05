from fastapi import APIRouter, Depends

from backend.auth import verify_token
from backend.schemas import EmployeeProfileUpdate
from backend.services import employee_profile_service

router = APIRouter(
    tags=["Employee Profile"]
)


@router.get("/employee/profile")
def get_profile(
    current_user: str = Depends(verify_token)
):
    return employee_profile_service.get_profile(current_user)


@router.put("/employee/profile")
def update_profile(
    profile: EmployeeProfileUpdate,
    current_user: str = Depends(verify_token)
):
    return employee_profile_service.update_profile(
        current_user,
        profile
    )