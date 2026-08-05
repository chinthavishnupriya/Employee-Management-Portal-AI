from pydantic import BaseModel

class PayrollCreate(BaseModel):
    employee_id: int
    basic_salary: float
    bonus: float = 0
    allowances: float
    deductions: float
    net_salary: float
    pay_date: str