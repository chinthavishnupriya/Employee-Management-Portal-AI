from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmployeeProfileUpdate(BaseModel):

    phone: Optional[str] = None

    address: Optional[str] = None

    emergency_contact: Optional[str] = None

    date_of_birth: Optional[date] = None

    joining_date: Optional[date] = None

    nationality: Optional[str] = None

    profile_photo: Optional[str] = None