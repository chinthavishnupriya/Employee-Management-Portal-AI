from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from backend.database import Base


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id")
    )

    leave_type = Column(
        String(50),
        nullable=False
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=False
    )

    reason = Column(String(255))

    status = Column(
        String(20),
        default="Pending"
    )

    employee = relationship("Employee")