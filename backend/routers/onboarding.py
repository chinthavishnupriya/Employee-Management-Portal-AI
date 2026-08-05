from fastapi import APIRouter, Depends

from backend.schemas import OnboardingCreate
from backend.auth import verify_admin, verify_token
from backend.models import User
from backend.services import onboarding_service

router = APIRouter(
    tags=["Onboarding"]
)


# ==========================
# Create Onboarding
# ==========================
@router.post("/onboarding")
def create_onboarding(
    onboarding: OnboardingCreate,
    admin: User = Depends(verify_admin)
):
    return onboarding_service.create_onboarding(onboarding)


# ==========================
# Get All Onboarding Records
# ==========================
@router.get("/onboarding")
def get_onboarding(
    current_user: str = Depends(verify_token)
):
    return onboarding_service.get_onboarding()


# ==========================
# Get Employee Onboarding
# ==========================
@router.get("/onboarding/{employee_id}")
def get_employee_onboarding(
    employee_id: int,
    current_user: str = Depends(verify_token)
):
    return onboarding_service.get_employee_onboarding(employee_id)


# ==========================
# Delete Onboarding
# ==========================
@router.delete("/onboarding/{onboarding_id}")
def delete_onboarding(
    onboarding_id: int,
    admin: User = Depends(verify_admin)
):
    return onboarding_service.delete_onboarding(onboarding_id)