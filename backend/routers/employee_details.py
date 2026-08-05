from fastapi import APIRouter, Depends

from backend.auth import verify_token
from backend.services import employee_details_service

router = APIRouter(
    tags=["Employee Details"]
)


@router.get("/employee/details")
def get_employee_details(
    current_user: str = Depends(verify_token)
):
    return employee_details_service.get_employee_details(
        current_user
    )