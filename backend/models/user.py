from sqlalchemy import Column, Integer, String
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(String(20), default="Employee")

    phone = Column(String(20), nullable=True)

    department = Column(String(100), nullable=True)

    designation = Column(String(100), nullable=True)

    profile_photo = Column(String(255), nullable=True)