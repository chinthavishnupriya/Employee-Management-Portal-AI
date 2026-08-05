from sqlalchemy.orm import Session

from backend.models.leave import LeaveRequest


class LeaveAI:

    def get_leave_summary(self, db: Session, employee_id: int):

        leaves = (
            db.query(LeaveRequest)
            .filter(LeaveRequest.employee_id == employee_id)
            .all()
        )

        pending = 0
        approved = 0
        rejected = 0

        history = []

        for leave in leaves:

            status = str(leave.status).lower()

            if status == "approved":
                approved += 1

            elif status == "pending":
                pending += 1

            elif status == "rejected":
                rejected += 1

            history.append(
                {
                    "type": leave.leave_type,
                    "start": str(leave.start_date),
                    "end": str(leave.end_date),
                    "status": leave.status
                }
            )

        return {
            "approved": approved,
            "pending": pending,
            "rejected": rejected,
            "history": history
        }


leave_ai = LeaveAI()