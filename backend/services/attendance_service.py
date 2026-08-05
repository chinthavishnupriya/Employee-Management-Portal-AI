from sqlalchemy.orm import Session
from datetime import datetime

from backend.database import SessionLocal
from backend.models import Attendance, Employee, User


# ==========================================
# Employee Check In
# ==========================================
def check_in(current_user):

    db: Session = SessionLocal()

    try:

        # Find logged-in user
        user = db.query(User).filter(
            User.email == current_user
        ).first()

        if user is None:
            return {
                "message": "User not found"
            }

        # Find employee using email
        employee = db.query(Employee).filter(
            Employee.email == current_user
        ).first()

        if employee is None:
            return {
                "message": "Employee not found"
            }

        today = datetime.now().date()

        # Already checked in today?
        attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee.id,
            Attendance.attendance_date == today
        ).first()

        if attendance:
            return {
                "message": "Already checked in today"
            }

        new_attendance = Attendance(
            employee_id=employee.id,
            attendance_date=today,
            check_in=datetime.now().time(),
            status="Present",
            attendance_type="Regular",
            working_hours=0,
            late_minutes=0,
            overtime_hours=0,
            remarks=""
        )

        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)

        return {
            "message": "Check-in successful",
            "attendance": new_attendance
        }

    except Exception as e:

        db.rollback()

        print("CHECK-IN ERROR:", e)

        raise

    finally:

        db.close()


# ==========================================
# Employee Check Out
# ==========================================
def check_out(current_user):

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
            Employee.email == current_user
        ).first()

        if employee is None:
            return {
                "message": "Employee not found"
            }

        attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee.id,
            Attendance.check_out == None
        ).first()

        if attendance is None:
            return {
                "message": "No active check-in found"
            }

        checkout = datetime.now()

        attendance.check_out = checkout.time()

        checkin = datetime.combine(
            checkout.date(),
            attendance.check_in
        )

        hours = (
            checkout - checkin
        ).total_seconds() / 3600

        attendance.working_hours = round(hours, 2)

        office_start = datetime.combine(
            checkout.date(),
            datetime.strptime(
                "09:00",
                "%H:%M"
            ).time()
        )

        if checkin > office_start:

            attendance.late_minutes = int(
                (checkin - office_start).total_seconds() / 60
            )

            attendance.status = "Late"

        else:

            attendance.status = "Present"

        if hours > 8:

            attendance.overtime_hours = round(
                hours - 8,
                2
            )

        else:

            attendance.overtime_hours = 0

        db.commit()
        db.refresh(attendance)

        return {

            "message": "Check-out successful",

            "attendance": attendance

        }

    except Exception as e:

        db.rollback()

        print("CHECK-OUT ERROR:", e)

        raise

    finally:

        db.close()


# ==========================================
# Admin - View All Attendance
# ==========================================
def get_all_attendance():

    db: Session = SessionLocal()

    try:

        attendance_list = db.query(Attendance).all()

        result = []

        for record in attendance_list:

            result.append({

                "id": record.id,

                "employee_id": record.employee.employee_id,

                "employee_name": record.employee.full_name,

                "department": record.employee.department.department_name,

                "date": record.attendance_date,

                "check_in": record.check_in,

                "check_out": record.check_out,

                "working_hours": record.working_hours,

                "late_minutes": record.late_minutes,

                "overtime_hours": record.overtime_hours,

                "attendance_type": record.attendance_type,

                "status": record.status,

                "remarks": record.remarks

            })

        return result

    finally:

        db.close()


# ==========================================
# Admin - Employee Attendance
# ==========================================
def get_employee_attendance(employee_id):

    db: Session = SessionLocal()

    try:

        attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee_id
        ).all()

        if not attendance:

            return {
                "message": "No attendance found"
            }

        result = []

        for record in attendance:

            result.append({

                "date": record.attendance_date,

                "employee_id": record.employee.employee_id,

                "employee_name": record.employee.full_name,

                "department": record.employee.department.department_name,

                "check_in": record.check_in,

                "check_out": record.check_out,

                "working_hours": record.working_hours,

                "late_minutes": record.late_minutes,

                "overtime_hours": record.overtime_hours,

                "attendance_type": record.attendance_type,

                "status": record.status,

                "remarks": record.remarks

            })

        return result

    finally:

        db.close()

def my_attendance(current_user):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.email == current_user
        ).first()

        if employee is None:
            return {
                "message": "Employee not found"
            }

        attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee.id
        ).all()

        result = []

        for record in attendance:

            result.append({

                "date": record.attendance_date,
                "check_in": record.check_in,
                "check_out": record.check_out,
                "working_hours": record.working_hours,
                "late_minutes": record.late_minutes,
                "overtime_hours": record.overtime_hours,
                "attendance_type": record.attendance_type,
                "status": record.status,
                "remarks": record.remarks

            })

        return result

    finally:

        db.close()

def my_summary(current_user):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.email == current_user
        ).first()

        if employee is None:
            return {
                "message": "Employee not found"
            }

        attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee.id
        ).all()

        present = sum(
            1 for a in attendance if a.status == "Present"
        )

        late = sum(
            1 for a in attendance if a.status == "Late"
        )

        total_hours = sum(
            a.working_hours or 0 for a in attendance
        )

        overtime = sum(
            a.overtime_hours or 0 for a in attendance
        )

        return {

            "total_days": len(attendance),

            "present": present,

            "late": late,

            "total_working_hours": round(total_hours, 2),

            "total_overtime": round(overtime, 2)

        }

    finally:

        db.close()

from datetime import date


def attendance_analytics():

    db: Session = SessionLocal()

    try:

        today = date.today()

        records = db.query(Attendance).all()

        today_records = [
            record
            for record in records
            if record.attendance_date == today
        ]

        present_today = sum(
            1
            for record in today_records
            if record.status == "Present"
        )

        late_today = sum(
            1
            for record in today_records
            if record.status == "Late"
        )

        absent_today = (
            db.query(Employee).count() -
            len(today_records)
        )

        total_hours = sum(
            record.working_hours or 0
            for record in records
        )

        total_overtime = sum(
            record.overtime_hours or 0
            for record in records
        )

        average_hours = 0

        if len(records) > 0:

            average_hours = round(
                total_hours / len(records),
                2
            )

        return {

            "present_today": present_today,

            "late_today": late_today,

            "absent_today": absent_today,

            "average_working_hours": average_hours,

            "total_overtime_hours": round(
                total_overtime,
                2
            )

        }

    finally:

        db.close()

def update_attendance(
    attendance_id,
    check_in,
    check_out
):

    db: Session = SessionLocal()

    try:

        attendance = db.query(Attendance).filter(
            Attendance.id == attendance_id
        ).first()

        if attendance is None:

            return {
                "message": "Attendance not found"
            }

        attendance.check_in = datetime.strptime(
            check_in,
            "%H:%M"
        ).time()

        attendance.check_out = datetime.strptime(
            check_out,
            "%H:%M"
        ).time()

        checkin = datetime.combine(
            datetime.today().date(),
            attendance.check_in
        )

        checkout = datetime.combine(
            datetime.today().date(),
            attendance.check_out
        )

        hours = (
            checkout - checkin
        ).total_seconds() / 3600

        attendance.working_hours = round(
            hours,
            2
        )

        office_start = datetime.combine(
            datetime.today().date(),
            datetime.strptime(
                "09:00",
                "%H:%M"
            ).time()
        )

        if checkin > office_start:

            attendance.late_minutes = int(
                (checkin - office_start).total_seconds() / 60
            )

            attendance.status = "Late"

        else:

            attendance.late_minutes = 0
            attendance.status = "Present"

        if hours > 8:

            attendance.overtime_hours = round(
                hours - 8,
                2
            )

        else:

            attendance.overtime_hours = 0

        db.commit()

        db.refresh(attendance)

        return {

            "message": "Attendance updated successfully",

            "attendance": attendance

        }

    except Exception as e:

        db.rollback()

        return {
            "error": str(e)
        }

    finally:

        db.close()