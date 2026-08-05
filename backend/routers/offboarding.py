from fastapi import APIRouter, Depends

from backend.schemas import OffboardingCreate
from backend.auth import verify_admin, verify_token
from backend.models import User
from backend.services import offboarding_service

router = APIRouter(
    tags=["Offboarding"]
)


@router.post("/offboarding")
def create_offboarding(
    offboarding: OffboardingCreate,
    admin: User = Depends(verify_admin)
):
    return offboarding_service.create_offboarding(offboarding)


@router.get("/offboarding")
def get_offboarding(
    current_user: str = Depends(verify_token)
):
    return offboarding_service.get_offboarding()


@router.get("/offboarding/{employee_id}")
def get_employee_offboarding(
    employee_id: int,
    current_user: str = Depends(verify_token)
):
    return offboarding_service.get_employee_offboarding(employee_id)


@router.delete("/offboarding/{offboarding_id}")
def delete_offboarding(
    offboarding_id: int,
    admin: User = Depends(verify_admin)
):
    return offboarding_service.delete_offboarding(offboarding_id)