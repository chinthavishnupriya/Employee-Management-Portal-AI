from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User
from backend.auth import verify_password, hash_password


def change_password(email, data):

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == email
        ).first()

        if user is None:
            return {
                "message": "User not found"
            }

        if not verify_password(
            data.current_password,
            user.password
        ):
            return {
                "message": "Current password is incorrect"
            }

        user.password = hash_password(
            data.new_password
        )

        db.commit()

        return {
            "message": "Password changed successfully"
        }

    finally:
        db.close()