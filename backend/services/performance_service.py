from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Performance, Employee


def create_performance(performance):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.id == performance.employee_id
        ).first()

        if employee is None:
            return {
                "message": "Employee not found"
            }

        new_review = Performance(
            employee_id=performance.employee_id,
            review_date=performance.review_date,
            rating=performance.rating,
            goals=performance.goals,
            strengths=performance.strengths,
            weaknesses=performance.weaknesses,
            feedback=performance.feedback,
            reviewer=performance.reviewer,
            promotion_status=performance.promotion_status
        )

        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        return {
            "message": "Performance review added successfully",
            "performance": new_review
        }

    finally:
        db.close()


def get_performance():

    db: Session = SessionLocal()

    try:

        reviews = db.query(Performance).all()

        result = []

        for review in reviews:

            result.append({

                "id": review.id,
                "employee": review.employee.full_name,
                "department": review.employee.department.department_name,
                "review_date": review.review_date,
                "rating": review.rating,
                "reviewer": review.reviewer,
                "promotion_status": review.promotion_status

            })

        return result

    finally:
        db.close()


def get_employee_performance(employee_id):

    db: Session = SessionLocal()

    try:

        reviews = db.query(Performance).filter(
            Performance.employee_id == employee_id
        ).all()

        return reviews

    finally:
        db.close()


def delete_performance(review_id):

    db: Session = SessionLocal()

    try:

        review = db.query(Performance).filter(
            Performance.id == review_id
        ).first()

        if review is None:
            return {
                "message": "Performance review not found"
            }

        db.delete(review)
        db.commit()

        return {
            "message": "Performance review deleted successfully"
        }

    finally:
        db.close()

from backend.models import User, Employee, Performance


def get_my_performance(current_user):

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == current_user
        ).first()

        if user is None:
            return {
                "message": "User not found"
            }

        employee = db.query(Employee).filter(
            Employee.email == user.email
        ).first()

        if employee is None:
            return {
                "message": "Employee not found"
            }

        reviews = db.query(Performance).filter(
            Performance.employee_id == employee.id
        ).all()

        result = []

        for review in reviews:

            result.append({

                "id": review.id,
                "review_date": review.review_date,
                "rating": review.rating,
                "reviewer": review.reviewer,
                "promotion_status": review.promotion_status,
                "goals": review.goals,
                "strengths": review.strengths,
                "weaknesses": review.weaknesses,
                "feedback": review.feedback

            })

        return result

    finally:
        db.close()