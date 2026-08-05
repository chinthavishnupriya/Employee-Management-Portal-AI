from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import pandas as pd

from backend.database import SessionLocal
from backend.models import Employee, Attendance, LeaveRequest, Payroll


def employee_report():

    db: Session = SessionLocal()

    try:

        employees = db.query(Employee).all()

        report = []

        for emp in employees:
            report.append({
                "Employee ID": emp.employee_id,
                "Name": emp.full_name,
                "Email": emp.email,
                "Department": emp.department.department_name,
                "Designation": emp.designation,
                "Salary": emp.salary
            })

        return {
            "total_employees": len(report),
            "employees": report
        }

    finally:
        db.close()


def attendance_report():

    db: Session = SessionLocal()

    try:

        records = db.query(Attendance).all()

        report = []

        for record in records:
            report.append({
                "Employee": record.employee.full_name,
                "Department": record.employee.department.department_name,
                "Date": record.attendance_date,
                "Check In": record.check_in,
                "Check Out": record.check_out,
                "Status": record.status
            })

        return report

    finally:
        db.close()


def export_employee_csv():

    db: Session = SessionLocal()

    try:

        employees = db.query(Employee).all()

        data = []

        for emp in employees:
            data.append({
                "Employee ID": emp.employee_id,
                "Name": emp.full_name,
                "Email": emp.email,
                "Department": emp.department.department_name,
                "Designation": emp.designation,
                "Salary": emp.salary
            })

        df = pd.DataFrame(data)

        file_name = "employees_report.csv"

        df.to_csv(file_name, index=False)

        return FileResponse(
            path=file_name,
            filename=file_name,
            media_type="text/csv"
        )

    finally:
        db.close()


def export_attendance_csv():

    db: Session = SessionLocal()

    try:

        records = db.query(Attendance).all()

        data = []

        for record in records:
            data.append({
                "Employee": record.employee.full_name,
                "Department": record.employee.department.department_name,
                "Date": record.attendance_date,
                "Check In": record.check_in,
                "Check Out": record.check_out,
                "Status": record.status
            })

        df = pd.DataFrame(data)

        file_name = "attendance_report.csv"

        df.to_csv(file_name, index=False)

        return FileResponse(
            path=file_name,
            filename=file_name,
            media_type="text/csv"
        )

    finally:
        db.close()


def export_leave_csv():

    db: Session = SessionLocal()

    try:

        leaves = db.query(LeaveRequest).all()

        data = []

        for leave in leaves:
            data.append({
                "Employee": leave.employee.full_name,
                "Department": leave.employee.department.department_name,
                "Leave Type": leave.leave_type,
                "From Date": leave.start_date,
                "To Date": leave.end_date,
                "Reason": leave.reason,
                "Status": leave.status
            })

        df = pd.DataFrame(data)

        file_name = "leave_report.csv"

        df.to_csv(file_name, index=False)

        return FileResponse(
            path=file_name,
            filename=file_name,
            media_type="text/csv"
        )

    finally:
        db.close()


def export_payroll_csv():

    db: Session = SessionLocal()

    try:

        payrolls = db.query(Payroll).all()

        data = []

        for payroll in payrolls:
            data.append({
                "Employee": payroll.employee.full_name,
                "Department": payroll.employee.department.department_name,
                "Basic Salary": payroll.basic_salary,
                "Bonus": payroll.bonus,
                "Deductions": payroll.deductions,
                "Net Salary": payroll.net_salary
            })

        df = pd.DataFrame(data)

        file_name = "payroll_report.csv"

        df.to_csv(file_name, index=False)

        return FileResponse(
            path=file_name,
            filename=file_name,
            media_type="text/csv"
        )

    finally:
        db.close()