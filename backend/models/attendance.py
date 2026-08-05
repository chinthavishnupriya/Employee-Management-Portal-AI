from sqlalchemy import Column, Integer, ForeignKey, Date, Time, String
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy import Float
from backend.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id")
    )

    attendance_date = Column(
        Date,
        default=date.today
    )

    check_in = Column(Time)

    check_out = Column(Time)

    status = Column(
        String(20),
        default="Present"
    )

    employee = relationship("Employee")
    working_hours = Column(
    Float,
    default=0
    )

    late_minutes = Column(
    Integer,
    default=0
    )

    overtime_hours = Column(
    Float,
    default=0
    )

    attendance_type = Column(
    String,
    default="Regular"
    )

    remarks = Column(
    String,
    nullable=True
    )