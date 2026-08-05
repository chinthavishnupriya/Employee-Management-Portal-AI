from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Payroll, Employee

from backend.database import SessionLocal
from backend.models import Payroll
from datetime import datetime

def create_payroll(data):

    db = SessionLocal()

    try:

        payroll = Payroll(
    employee_id=data.employee_id,
    basic_salary=data.basic_salary,
    bonus=data.bonus,
    allowances=data.allowances,
    deductions=data.deductions,
    net_salary=data.net_salary,
    pay_date=datetime.strptime(
        data.pay_date,
        "%Y-%m-%d"
    ).date()
)

        db.add(payroll)
        db.commit()
        db.refresh(payroll)

        return {
            "message": "Payroll created successfully",
            "payroll": payroll
        }

    finally:
        db.close()
def get_my_payroll(email):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.email == email
        ).first()

        if employee is None:
            return []

        payrolls = db.query(Payroll).filter(
            Payroll.employee_id == employee.id
        ).all()

        result = []

        for payroll in payrolls:

            result.append({

                "id": payroll.id,
                "basic_salary": payroll.basic_salary,
                "bonus": payroll.bonus,
                "allowances": payroll.allowances,
                "deductions": payroll.deductions,
                "net_salary": payroll.net_salary,
                "pay_date": payroll.pay_date

            })

        return result

    finally:
        db.close()
def get_payrolls():

    db: Session = SessionLocal()

    try:

        payrolls = db.query(Payroll).all()

        result = []

        for payroll in payrolls:

            employee = db.query(Employee).filter(
                Employee.id == payroll.employee_id
            ).first()

            result.append({

                "id": payroll.id,

                "employee_id": payroll.employee_id,

                "employee": employee.full_name if employee else "",

                "department": employee.department.department_name
                if employee and employee.department else "",

                "basic_salary": payroll.basic_salary,

                "bonus": payroll.bonus,

                "allowances": payroll.allowances,

                "deductions": payroll.deductions,

                "net_salary": payroll.net_salary,

                "pay_date": payroll.pay_date

            })

        return result

    finally:
        db.close()

def get_payroll(payroll_id):

    db = SessionLocal()

    try:

        payroll = db.query(Payroll).filter(
            Payroll.id == payroll_id
        ).first()

        if payroll is None:
            return {"message": "Payroll not found"}

        return payroll

    finally:
        db.close()

def update_payroll(payroll_id, data):

    db = SessionLocal()

    try:

        payroll = db.query(Payroll).filter(
            Payroll.id == payroll_id
        ).first()

        if payroll is None:
            return {
                "message": "Payroll not found"
            }

        payroll.employee_id = data.employee_id
        payroll.basic_salary = data.basic_salary
        payroll.bonus = data.bonus
        payroll.allowances = data.allowances
        payroll.deductions = data.deductions
        payroll.net_salary = data.net_salary
        payroll.pay_date = datetime.strptime(
            data.pay_date,
            "%Y-%m-%d"
        ).date()

        db.commit()
        db.refresh(payroll)

        return {
            "message": "Payroll updated successfully",
            "payroll": payroll
        }

    finally:
        db.close()

def delete_payroll(payroll_id):

    db = SessionLocal()

    try:

        payroll = db.query(Payroll).filter(
            Payroll.id == payroll_id
        ).first()

        if payroll is None:
            return {
                "message": "Payroll not found"
            }

        db.delete(payroll)
        db.commit()

        return {
            "message": "Payroll deleted successfully"
        }

    finally:
        db.close()