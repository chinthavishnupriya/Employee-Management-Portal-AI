from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    review_date = Column(Date, nullable=False)

    rating = Column(Integer, nullable=False)

    goals = Column(String, nullable=True)

    strengths = Column(String, nullable=True)

    weaknesses = Column(String, nullable=True)

    feedback = Column(String, nullable=True)

    reviewer = Column(String, nullable=False)

    promotion_status = Column(
        String,
        default="Not Reviewed"
    )

    employee = relationship(
        "Employee",
        back_populates="performance_records"
    )