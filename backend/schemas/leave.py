from pydantic import BaseModel


class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: str
    end_date: str
    reason: str