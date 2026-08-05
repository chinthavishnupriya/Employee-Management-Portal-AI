from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: str
    department_id: int
    designation: str
    salary: float