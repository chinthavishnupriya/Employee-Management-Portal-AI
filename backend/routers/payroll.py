from fastapi import APIRouter, Depends

from backend.auth import verify_token, verify_admin
from backend.models import User
from backend.services import payroll_service

router = APIRouter(
    tags=["Payroll Management"]
)


# ==========================
# Employee - My Payroll
# ==========================
@router.get("/payroll/me")
def get_my_payroll(
    current_user: str = Depends(verify_token)
):
    return payroll_service.get_my_payroll(current_user)


# ==========================
# Admin - All Payroll
# ==========================
@router.get("/payroll")
def get_payrolls(
    admin: User = Depends(verify_admin)
):
    return payroll_service.get_payrolls()
from backend.schemas import PayrollCreate

# ==========================
# Admin - Create Payroll
# ==========================
@router.post("/payroll")
def create_payroll(
    payroll: PayrollCreate,
    admin: User = Depends(verify_admin)
):
    return payroll_service.create_payroll(payroll)
# ==========================
# Admin - Get Payroll by ID
# ==========================
@router.get("/payroll/{payroll_id}")
def get_payroll(
    payroll_id: int,
    admin: User = Depends(verify_admin)
):
    return payroll_service.get_payroll(payroll_id)


# ==========================
# Admin - Update Payroll
# ==========================
@router.put("/payroll/{payroll_id}")
def update_payroll(
    payroll_id: int,
    payroll: PayrollCreate,
    admin: User = Depends(verify_admin)
):
    return payroll_service.update_payroll(payroll_id, payroll)


# ==========================
# Admin - Delete Payroll
# ==========================
@router.delete("/payroll/{payroll_id}")
def delete_payroll(
    payroll_id: int,
    admin: User = Depends(verify_admin)
):
    return payroll_service.delete_payroll(payroll_id)