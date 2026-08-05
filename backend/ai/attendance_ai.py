from sqlalchemy.orm import Session
from backend.models import Attendance


class AttendanceAI:

    def get_attendance_summary(self, db: Session, employee_id: int):

        records = (
            db.query(Attendance)
            .filter(Attendance.employee_id == employee_id)
            .all()
        )

        present = 0
        absent = 0
        late = 0
        leave = 0

        for record in records:

            status = str(record.status).lower()

            if status == "present":
                present += 1

            elif status == "absent":
                absent += 1

            elif status == "late":
                late += 1

            elif status == "leave":
                leave += 1

        summary = {
            "present": present,
            "absent": absent,
            "late": late,
            "leave": leave
        }

        print("RETURNING:", summary)

        return summary


attendance_ai = AttendanceAI()