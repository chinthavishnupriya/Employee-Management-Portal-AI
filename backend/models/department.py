from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    department_name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    description = Column(String(255))

    employees = relationship(
        "Employee",
        back_populates="department"
    )