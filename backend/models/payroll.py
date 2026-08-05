from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from backend.database import Base


class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id")
    )

    basic_salary = Column(
        Float,
        nullable=False
    )

    bonus = Column(
        Float,
        default=0
    )

    allowances = Column(
        Float,
        default=0
    )

    deductions = Column(
        Float,
        default=0
    )

    net_salary = Column(
        Float,
        nullable=False
    )

    pay_date = Column(Date)

    employee = relationship("Employee")