from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class Offboarding(Base):
    __tablename__ = "offboarding"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    resignation_date = Column(Date)

    last_working_day = Column(Date)

    exit_reason = Column(String)

    laptop_returned = Column(Boolean, default=False)

    id_card_returned = Column(Boolean, default=False)

    account_disabled = Column(Boolean, default=False)

    exit_interview_completed = Column(Boolean, default=False)

    final_settlement_completed = Column(Boolean, default=False)

    status = Column(
        String,
        default="In Progress"
    )

    employee = relationship(
        "Employee",
        back_populates="offboarding_records"
    )