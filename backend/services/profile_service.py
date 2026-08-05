from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import User


def get_profile(email):

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            return {
                "message": "User not found"
            }

        return {

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


def update_profile(email, profile):

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            return {
                "message": "User not found"
            }

        user.username = profile.username
        user.phone = profile.phone
        user.department = profile.department
        user.designation = profile.designation

        db.commit()
        db.refresh(user)

        return {

            "message": "Profile updated successfully"

        }

    finally:

        db.close()




def update_profile_photo(email, photo_path):

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == email
        ).first()

        if user is None:

            return {
                "message": "User not found"
            }

        user.profile_photo = photo_path

        db.commit()

        db.refresh(user)

        return {
            "message": "Profile photo updated successfully"
        }

    finally:

        db.close()