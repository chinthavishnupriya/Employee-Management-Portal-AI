from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Onboarding, Employee


# ==========================================
# Create Onboarding
# ==========================================

def create_onboarding(onboarding):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.id == onboarding.employee_id
        ).first()

        if employee is None:

            return {
                "message": "Employee not found"
            }

        new_onboarding = Onboarding(

            employee_id=onboarding.employee_id,

            offer_status=onboarding.offer_status,

            documents_uploaded=onboarding.documents_uploaded,

            email_created=onboarding.email_created,

            id_card_issued=onboarding.id_card_issued,

            laptop_assigned=onboarding.laptop_assigned,

            orientation_completed=onboarding.orientation_completed,

            manager_assigned=onboarding.manager_assigned,

            status=onboarding.status,

            joining_date=onboarding.joining_date,

            mentor=onboarding.mentor,

            training_status=onboarding.training_status,

            welcome_kit=onboarding.welcome_kit

        )

        db.add(new_onboarding)

        db.commit()

        db.refresh(new_onboarding)

        return {

            "message": "Onboarding created successfully",

            "onboarding": new_onboarding

        }

    finally:

        db.close()


# ==========================================
# Get All Onboarding Records
# ==========================================

def get_onboarding():

    db: Session = SessionLocal()

    try:

        records = db.query(Onboarding).all()

        result = []

        for record in records:

            result.append({

                "id": record.id,

                "employee": record.employee.full_name,

                "department": record.employee.department.department_name,

                "offer_status": record.offer_status,

                "documents_uploaded": record.documents_uploaded,

                "email_created": record.email_created,

                "id_card_issued": record.id_card_issued,

                "laptop_assigned": record.laptop_assigned,

                "orientation_completed": record.orientation_completed,

                "manager_assigned": record.manager_assigned,

                "status": record.status,

                "joining_date": record.joining_date,

                "mentor": record.mentor,

                "training_status": record.training_status,

                "welcome_kit": record.welcome_kit

            })

        return result

    finally:

        db.close()


# ==========================================
# Get Employee Onboarding
# ==========================================

def get_employee_onboarding(employee_id):

    db: Session = SessionLocal()

    try:

        records = db.query(Onboarding).filter(
            Onboarding.employee_id == employee_id
        ).all()

        return records

    finally:

        db.close()


# ==========================================
# Delete Onboarding
# ==========================================

def delete_onboarding(onboarding_id):

    db: Session = SessionLocal()

    try:

        record = db.query(Onboarding).filter(
            Onboarding.id == onboarding_id
        ).first()

        if record is None:

            return {
                "message": "Onboarding record not found"
            }

        db.delete(record)

        db.commit()

        return {

            "message": "Onboarding deleted successfully"

        }

    finally:

        db.close()