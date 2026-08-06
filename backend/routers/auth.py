from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.database import SessionLocal
from backend.models import User, Employee
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
        return {"error": str(e)}

    finally:
        db.close()


# ==========================
# Login
# ==========================
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db: Session = SessionLocal()

    try:

        print("\n" + "=" * 70)
        print("LOGIN REQUEST")
        print("=" * 70)

        email = form_data.username.strip().lower()

        print("Entered Email :", repr(email))

        # -----------------------------
        # Database Information
        # -----------------------------
        print("\nDATABASE INFORMATION")

        print(
            "Current Database:",
            db.execute(
                text("SELECT current_database()")
            ).scalar()
        )

        print(
            "Current User:",
            db.execute(
                text("SELECT current_user")
            ).scalar()
        )

        print(
            "Server Address:",
            db.execute(
                text("SELECT inet_server_addr()")
            ).scalar()
        )

        print(
            "Server Port:",
            db.execute(
                text("SELECT inet_server_port()")
            ).scalar()
        )

        # -----------------------------
        # User Count
        # -----------------------------
        total = db.query(User).count()
        print("\nTOTAL USERS:", total)

        users = db.query(User).all()

        print("\nUSERS TABLE")
        print("-" * 70)

        if not users:
            print("No users found.")
        else:
            for u in users:
                print(
                    f"ID={u.id} | "
                    f"Username={u.username} | "
                    f"Email={u.email} | "
                    f"Role={u.role}"
                )

        print("-" * 70)

        # -----------------------------
        # Search User
        # -----------------------------
        print("\nSearching user...")

        db_user = (
            db.query(User)
            .filter(User.email.ilike(email))
            .first()
        )

        print("Matched User:", db_user)

        if db_user is None:
            print("EMAIL NOT FOUND")
            return {
                "message": "Invalid email"
            }

        # -----------------------------
        # Password Check
        # -----------------------------
        password_ok = verify_password(
            form_data.password,
            db_user.password
        )

        print("Password Match:", password_ok)

        if not password_ok:
            return {
                "message": "Invalid password"
            }

        # -----------------------------
        # Employee Lookup
        # -----------------------------
        emp = (
            db.query(Employee)
            .filter(Employee.email == db_user.email)
            .first()
        )

        print("Employee:", emp)

        # -----------------------------
        # JWT Token
        # -----------------------------
        token = create_access_token(
            {
                "sub": db_user.email
            }
        )

        print("LOGIN SUCCESS")
        print("=" * 70)

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": db_user.role,
            "employee_id": emp.id if emp else None,
            "user": {
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email,
                "role": db_user.role
            }
        }

    finally:
        db.close()