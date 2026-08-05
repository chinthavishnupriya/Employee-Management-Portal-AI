import os

from fastapi import APIRouter, Depends, UploadFile, File

from backend.auth import verify_token
from backend.services import profile_photo_service

router = APIRouter(
    tags=["Employee Profile"]
)


@router.post("/employee/profile-photo")
async def upload_profile_photo(
    photo: UploadFile = File(...),
    current_user: str = Depends(verify_token)
):
    return await profile_photo_service.upload_photo(
        current_user,
        photo
    )