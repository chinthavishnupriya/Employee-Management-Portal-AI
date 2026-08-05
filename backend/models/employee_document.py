from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database import Base

class EmployeeDocument(Base):

    __tablename__ = "employee_documents"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False
    )

    document_type = Column(
        String(50),
        nullable=False
    )

    document_name = Column(
        String(255)
    )

    file_path = Column(
        Text,
        nullable=False
    )

    status = Column(
        String(20),
        default="Pending"
    )

    remarks = Column(
        Text
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    employee = relationship(
        "Employee",
        back_populates="documents"
    )