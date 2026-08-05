from fastapi import APIRouter
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import (
    Employee,
    Department,
    Attendance,
    LeaveRequest,
    Payroll,
    Performance
)

router = APIRouter(tags=["Home"])


@router.get("/home")
def home_data():

    db: Session = SessionLocal()

    try:

        total_employees = db.query(Employee).count()

        total_departments = db.query(Department).count()

        total_attendance = db.query(Attendance).count()

        total_leaves = db.query(LeaveRequest).count()

        return {

            "portal_name": "AI Employee Management Portal",

            "hero": {
                "title": "Modern HR Management Platform",
                "subtitle": "Manage Employees, Attendance, Payroll, Leave, Performance and AI Analytics from one secure platform."
            },

            "statistics": {

                "employees": total_employees,

                "departments": total_departments,

                "attendance": total_attendance,

                "leave_requests": total_leaves

            },

            "features": [

                {
                    "title": "Employee Management",
                    "icon": "👨‍💼",
                    "description": "Manage employee records."
                },

                {
                    "title": "Attendance",
                    "icon": "⏰",
                    "description": "Track employee attendance."
                },

                {
                    "title": "Payroll",
                    "icon": "💰",
                    "description": "Manage payroll records."
                },

                {
                    "title": "Performance",
                    "icon": "📈",
                    "description": "Evaluate employee performance."
                },

                {
                    "title": "Documents",
                    "icon": "📄",
                    "description": "Secure document management."
                },

                {
                    "title": "AI Analytics",
                    "icon": "🤖",
                    "description": "Business insights using AI."
                }

            ]

        }

    finally:

        db.close()