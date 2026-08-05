from pydantic import BaseModel
from datetime import datetime


class EmployeeDocumentResponse(BaseModel):

    id: int
    employee_id: int
    document_type: str
    document_name: str
    file_path: str
    status: str
    remarks: str | None = None
    uploaded_at: datetime

    class Config:
        from_attributes = True