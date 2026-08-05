from pydantic import BaseModel
from datetime import date


class OffboardingCreate(BaseModel):
    employee_id: int
    resignation_date: date
    last_working_day: date
    exit_reason: str
    laptop_returned: bool
    id_card_returned: bool
    account_disabled: bool
    exit_interview_completed: bool
    final_settlement_completed: bool
    status: str


class OffboardingResponse(BaseModel):
    id: int
    employee_id: int
    resignation_date: date
    last_working_day: date
    exit_reason: str
    laptop_returned: bool
    id_card_returned: bool
    account_disabled: bool
    exit_interview_completed: bool
    final_settlement_completed: bool
    status: str

    class Config:
        from_attributes = True