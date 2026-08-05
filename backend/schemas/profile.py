from pydantic import BaseModel
from typing import Optional


class ProfileResponse(BaseModel):
    username: str
    email: str
    role: str
    phone: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    profile_photo: Optional[str] = None

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    username: str
    phone: str
    department: str
    designation: str