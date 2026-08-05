from datetime import date
from pydantic import BaseModel


class OnboardingCreate(BaseModel):
    employee_id: int
    offer_status: str
    documents_uploaded: bool
    email_created: bool
    id_card_issued: bool
    laptop_assigned: bool
    orientation_completed: bool
    manager_assigned: bool
    status: str

    joining_date: date | None = None
    mentor: str | None = None
    training_status: str | None = None
    welcome_kit: str | None = None


class OnboardingResponse(BaseModel):
    id: int
    employee_id: int
    offer_status: str
    documents_uploaded: bool
    email_created: bool
    id_card_issued: bool
    laptop_assigned: bool
    orientation_completed: bool
    manager_assigned: bool
    status: str

    joining_date: date | None = None
    mentor: str | None = None
    training_status: str | None = None
    welcome_kit: str | None = None

    class Config:
        from_attributes = True