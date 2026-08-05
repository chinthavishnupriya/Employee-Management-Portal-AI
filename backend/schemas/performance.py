from pydantic import BaseModel
from datetime import date


class PerformanceCreate(BaseModel):
    employee_id: int
    review_date: date
    rating: int
    goals: str
    strengths: str
    weaknesses: str
    feedback: str
    reviewer: str
    promotion_status: str


class PerformanceResponse(BaseModel):
    id: int
    employee_id: int
    review_date: date
    rating: int
    goals: str
    strengths: str
    weaknesses: str
    feedback: str
    reviewer: str
    promotion_status: str

    class Config:
        from_attributes = True