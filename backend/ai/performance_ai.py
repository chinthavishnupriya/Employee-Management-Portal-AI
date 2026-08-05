from sqlalchemy.orm import Session

from backend.models.performance import Performance


class PerformanceAI:

    def get_performance_summary(self, db: Session, employee_id: int):

        performance = (
            db.query(Performance)
            .filter(Performance.employee_id == employee_id)
            .order_by(Performance.review_date.desc())
            .first()
        )

        if performance is None:
            return None

        return {
            "rating": performance.rating,
            "review_date": str(performance.review_date),
            "goals": performance.goals,
            "strengths": performance.strengths,
            "weaknesses": performance.weaknesses,
            "feedback": performance.feedback,
            "reviewer": performance.reviewer,
            "promotion_status": performance.promotion_status
        }


performance_ai = PerformanceAI()