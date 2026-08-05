from sqlalchemy import Column, Date, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base
from sqlalchemy import Date

class Onboarding(Base):
    __tablename__ = "onboarding"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    offer_status = Column(String, default="Pending")

    documents_uploaded = Column(Boolean, default=False)

    email_created = Column(Boolean, default=False)

    id_card_issued = Column(Boolean, default=False)

    laptop_assigned = Column(Boolean, default=False)

    orientation_completed = Column(Boolean, default=False)

    manager_assigned = Column(Boolean, default=False)

    status = Column(
        String,
        default="In Progress"
    )

    employee = relationship(
        "Employee",
        back_populates="onboarding_records"
    )
    

    joining_date = Column(
        Date,
        nullable=True
    )

    mentor = Column(
         String(100),
        nullable=True
    )

    training_status = Column(
        String(50),
        nullable=True
    )

    welcome_kit = Column(
        String(50),
        nullable=True
    )