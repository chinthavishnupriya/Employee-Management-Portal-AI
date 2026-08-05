from pydantic import BaseModel
from typing import Optional

remarks: Optional[str] = None

class AttendanceCreate(BaseModel):
    employee_id: int
    working_hours: float = 0
    late_minutes: int = 0
    overtime_hours: float = 0
    attendance_type: str = "Regular"
    remarks: str | None = None