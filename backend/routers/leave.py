from fastapi import APIRouter, Depends

from backend.schemas import LeaveRequestCreate
from backend.auth import verify_token, verify_admin
from backend.models import User
from backend.services import leave_service

router = APIRouter(
    tags=["Leave Management"]
)


@router.post("/leave/apply")
def apply_leave(
    leave: LeaveRequestCreate,
    current_user: str = Depends(verify_token)
):
    return leave_service.apply_leave(leave)
@router.get("/leave/me")
def my_leaves(
    current_user: str = Depends(verify_token)
):
    return leave_service.get_my_leaves(current_user)


@router.delete("/leave/{leave_id}")
def cancel_leave(
    leave_id: int,
    current_user: str = Depends(verify_token)
):
    return leave_service.cancel_leave(leave_id)

@router.get("/leave")
def get_leave_requests(
    current_user: str = Depends(verify_token)
):
    return leave_service.get_leave_requests()


@router.put("/leave/approve/{leave_id}")
def approve_leave(
    leave_id: int,
    admin: User = Depends(verify_admin)
):
    return leave_service.approve_leave(leave_id)


@router.put("/leave/reject/{leave_id}")
def reject_leave(
    leave_id: int,
    admin: User = Depends(verify_admin)
):
    return leave_service.reject_leave(leave_id)