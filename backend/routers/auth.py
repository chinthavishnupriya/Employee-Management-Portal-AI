from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import User, Employee, employee
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token
)
from backend.schemas import UserCreate

router = APIRouter(
    tags=["Authentication"]
)


# ==========================
# Register
# ==========================
@router.post("/register")
def register(user: UserCreate):
    db: Session = SessionLocal()

    try:
        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
            role=user.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user_id": new_user.id
        }

    except Exception as e:
        db.rollback()
        return {
            "error": str(e)
        }

    finally:
        db.close()


# ==========================
# Login
# ==========================
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db: Session = SessionLocal()

    try:
        print("=" * 50)
        print("Entered Email:", repr(form_data.username))

        users = db.query(User).all()

        print("Users in Database:")
        for user in users:
            print(repr(user.email))

        db_user = db.query(User).filter(
            User.email == form_data.username.strip()
        ).first()

        print("Matched User:", db_user)

        if db_user is None:
            return {
                "message": "Invalid email"
            }

        if not verify_password(
            form_data.password,
            db_user.password
        ):
            return {
                "message": "Invalid password"
            }

        # Find employee record
        employee = db.query(Employee).filter(
            Employee.email == db_user.email
        ).first()

        token = create_access_token(
            {"sub": db_user.email}
        )
        print("Logged in user:", db_user.email)
        print("Employee:", employee)
        print("Employee ID:", employee.id if employee else None)
        return {
            "access_token": token,
            "token_type": "bearer",
            "role": db_user.role,
            "employee_id": employee.id if employee else None,
            "user": {
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email,
                "role": db_user.role
            }
        }

    finally:
        db.close()