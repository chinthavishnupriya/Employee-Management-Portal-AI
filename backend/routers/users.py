from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import SessionLocal
from backend.models import User
from backend.auth import verify_token, hash_password

router = APIRouter(
    tags=["Users"]
)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "Employee"


@router.get("/users")
def get_users(current_user: str = Depends(verify_token)):
    db: Session = SessionLocal()

    try:
        users = db.query(User).all()
        return users

    finally:
        db.close()


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    current_user: str = Depends(verify_token)
):
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return {
                "message": "User not found"
            }

        return user

    finally:
        db.close()


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserCreate,
    current_user: str = Depends(verify_token)
):
    db: Session = SessionLocal()

    try:
        existing_user = db.query(User).filter(
            User.id == user_id
        ).first()

        if existing_user is None:
            return {
                "message": "User not found"
            }

        existing_user.username = user.username
        existing_user.email = user.email
        existing_user.password = hash_password(user.password)
        existing_user.role = user.role

        db.commit()
        db.refresh(existing_user)

        return {
            "message": "User updated successfully",
            "user": existing_user
        }

    finally:
        db.close()


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: str = Depends(verify_token)
):
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user is None:
            return {
                "message": "User not found"
            }

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully"
        }

    finally:
        db.close()