from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Offboarding, Employee


def create_offboarding(offboarding):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.id == offboarding.employee_id
        ).first()

        if employee is None:
            return {
                "message": "Employee not found"
            }

        new_offboarding = Offboarding(
            employee_id=offboarding.employee_id,
            resignation_date=offboarding.resignation_date,
            last_working_day=offboarding.last_working_day,
            exit_reason=offboarding.exit_reason,
            laptop_returned=offboarding.laptop_returned,
            id_card_returned=offboarding.id_card_returned,
            account_disabled=offboarding.account_disabled,
            exit_interview_completed=offboarding.exit_interview_completed,
            final_settlement_completed=offboarding.final_settlement_completed,
            status=offboarding.status
        )

        db.add(new_offboarding)
        db.commit()
        db.refresh(new_offboarding)

        return {
            "message": "Offboarding created successfully",
            "offboarding": new_offboarding
        }

    finally:
        db.close()


def get_offboarding():

    db: Session = SessionLocal()

    try:

        records = db.query(Offboarding).all()

        result = []

        for record in records:

            result.append({

                "id": record.id,
                "employee": record.employee.full_name,
                "department": record.employee.department.department_name,
                "resignation_date": record.resignation_date,
                "last_working_day": record.last_working_day,
                "exit_reason": record.exit_reason,
                "status": record.status

            })

        return result

    finally:
        db.close()


def get_employee_offboarding(employee_id):

    db: Session = SessionLocal()

    try:

        records = db.query(Offboarding).filter(
            Offboarding.employee_id == employee_id
        ).all()

        return records

    finally:
        db.close()


def delete_offboarding(offboarding_id):

    db: Session = SessionLocal()

    try:

        record = db.query(Offboarding).filter(
            Offboarding.id == offboarding_id
        ).first()

        if record is None:
            return {
                "message": "Offboarding record not found"
            }

        db.delete(record)
        db.commit()

        return {
            "message": "Offboarding deleted successfully"
        }

    finally:
        db.close()