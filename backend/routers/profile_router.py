from fastapi import APIRouter, Depends

from backend.auth import verify_token
from backend.schemas import ProfileUpdate
from backend.services import profile_service
from fastapi import UploadFile, File
import shutil
import os
router = APIRouter(
    tags=["Profile"]
)


# ==========================
# Get Profile
# ==========================

@router.get("/profile")
def get_profile(
    current_user: str = Depends(verify_token)
):

    return profile_service.get_profile(current_user)


# ==========================
# Update Profile
# ==========================

@router.put("/profile")
def update_profile(
    profile: ProfileUpdate,
    current_user: str = Depends(verify_token)
):

    return profile_service.update_profile(
        current_user,
        profile
    )

@router.post("/profile/upload-photo")
def upload_profile_photo(
    file: UploadFile = File(...),
    current_user: str = Depends(verify_token)
):

    folder = "backend/uploads/profile"

    os.makedirs(folder, exist_ok=True)

    filename = current_user.replace("@", "_") + "_" + file.filename

    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    profile_service.update_profile_photo(

        current_user,

        "/" + filepath.replace("\\", "/")

    )

    return {

        "message": "Photo uploaded successfully",

        "photo": "/" + filepath.replace("\\", "/")

    }