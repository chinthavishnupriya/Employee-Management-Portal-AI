from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# Secret key (change this later in production)
SECRET_KEY = "employee_management_secret_key"

# JWT Algorithm
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Token expires in 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 10080

# Password Hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
def verify_token(token: str = Depends(oauth2_scheme)):
    print("=" * 50)
    print("Received Token:", repr(token))

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("Payload:", payload)

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
            )

        return email

    except JWTError as e:
        print("JWT Error:", str(e))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User

def verify_admin(current_user: str = Depends(verify_token)):
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == current_user
        ).first()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if user.role != "Admin":
            raise HTTPException(
                status_code=403,
                detail="Only Admin can perform this action"
            )

        return user

    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    db: Session = SessionLocal()

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = db.query(User).filter(
            User.email == email
        ).first()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    finally:
        db.close()