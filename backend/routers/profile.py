from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.auth import verify_token
from backend.models import User

router = APIRouter(
    tags=["Profile"]
)


@router.get("/profile")
def get_profile(
    current_user: str = Depends(verify_token)
):
    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == current_user
        ).first()

        if user is None:
            return {
                "message": "User not found"
            }

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "phone": user.phone,
            "department": user.department,
            "designation": user.designation,
            "profile_photo": user.profile_photo
        }

    finally:
        db.close()