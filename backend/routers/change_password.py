from fastapi import APIRouter, Depends

from backend.auth import verify_token
from backend.schemas.user import ChangePassword
from backend.services import change_password_service

router = APIRouter(
    tags=["Change Password"]
)


@router.put("/change-password")
def change_password(
    data: ChangePassword,
    current_user: str = Depends(verify_token)
):
    return change_password_service.change_password(
        current_user,
        data
    )