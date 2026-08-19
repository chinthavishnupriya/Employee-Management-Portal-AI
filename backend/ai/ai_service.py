import re
from datetime import date, timedelta
from sqlalchemy import func
from backend.models import Attendance, LeaveRequest, Payroll, Performance, EmployeeDocument

from backend.ai.llm_service import llm
from backend.ai.attendance_ai import attendance_ai
from backend.ai.payroll_ai import payroll_ai
from backend.ai.leave_ai import leave_ai
from backend.ai.profile_ai import profile_ai
from backend.ai.performance_ai import performance_ai
from backend.models import (
    Employee,
    Department,
    Attendance,
    LeaveRequest,
    Payroll,
    Performance,
    Onboarding,
    Offboarding
)


class AIService:
    """
    Handles all AI-related business logic.
    Calls the local LLM service.
    """

    def ask(self, prompt: str, db=None, employee_id=None):

        prompt = prompt.strip()

        if not prompt:
            return "Please enter your question."

        prompt_lower = prompt.lower()

        # ==========================================
        # EMPLOYEE PRIORITY ROUTING
        # ==========================================
        # Handle explicit "my ..." questions before
        # generic/admin database AI branches.
        #
        # This prevents employee questions such as:
        #   What is my performance?
        #   What is my department?
        # from being interpreted as admin-wide queries.

        if (
            db is not None
            and employee_id is not None
            and (
                "my department" in prompt_lower
                or "my performance" in prompt_lower
                or "my rating" in prompt_lower
                or "my goals" in prompt_lower
                or "my strengths" in prompt_lower
                or "my weaknesses" in prompt_lower
                or "my feedback" in prompt_lower
                or "my reviewer" in prompt_lower
                or "my promotion" in prompt_lower
                or "promotion status" in prompt_lower
                or "eligible for promotion" in prompt_lower
                or "my salary" in prompt_lower
                or "my deductions" in prompt_lower
                or "my payroll" in prompt_lower
                or "my onboarding" in prompt_lower
                or "my offboarding" in prompt_lower
                or "my attendance" in prompt_lower
                or "my leave" in prompt_lower
                or "my leaves" in prompt_lower
                or "salary" in prompt_lower
                or "payroll" in prompt_lower
                or "performance" in prompt_lower
                or "attendance" in prompt_lower
                or "leave" in prompt_lower
                or "onboarding" in prompt_lower
                or "offboarding" in prompt_lower
                or "department" in prompt_lower
            )
        ):

            employee = (
                db.query(Employee)
                .filter(Employee.id == employee_id)
                .first()
            )

            if employee is None:
                return "Employee profile not found."

            # ==========================================
            # EMPLOYEE SECURITY: BLOCK OTHER EMPLOYEES
            # ==========================================
            # Employees may access only their own HR data.
            # If another employee's name appears in the
            # question, do not allow the request to fall
            # through to generic AI/database logic.

            all_employees = db.query(Employee).all()

            for other_employee in all_employees:

                if other_employee.id == employee.id:
                    continue

                other_full_name = (
                    other_employee.full_name or ""
                ).strip().lower()

                if not other_full_name:
                    continue

                name_parts = other_full_name.split()

                # Match full name, e.g. "rahul kumar"
                if other_full_name in prompt_lower:
                    return (
                        "Sorry, you are not authorized to access "
                        "other employees' information."
                    )

                # Match first name, e.g. "Rahul's salary"
                if name_parts:
                    first_name = name_parts[0]

                    if (
                        len(first_name) >= 3
                        and re.search(
                            rf"\b{re.escape(first_name)}\b",
                            prompt_lower
                        )
                    ):
                        return (
                            "Sorry, you are not authorized to access "
                            "other employees' information."
                        )

            # ------------------------------------------
            # My Department
            # ------------------------------------------

            if "my department" in prompt_lower:

                department_name = (
                    employee.department.department_name
                    if employee.department
                    else "Not assigned"
                )

                return (
                    f"Your department is {department_name}."
                )

            # ------------------------------------------
            # My Performance
            # ------------------------------------------

            if (
                "my performance" in prompt_lower
                or "my rating" in prompt_lower
                or "my goals" in prompt_lower
                or "my strengths" in prompt_lower
                or "my weaknesses" in prompt_lower
                or "my feedback" in prompt_lower
                or "my reviewer" in prompt_lower
                or "my promotion" in prompt_lower
                or "promotion status" in prompt_lower
                or "eligible for promotion" in prompt_lower
            ):

                record = (
                    db.query(Performance)
                    .filter(
                        Performance.employee_id == employee.id
                    )
                    .order_by(
                        Performance.review_date.desc(),
                        Performance.id.desc()
                    )
                    .first()
                )

                if not record:
                    return (
                        f"No performance record found for "
                        f"{employee.full_name}."
                    )

                # ------------------------------------------
                # Specific performance questions
                # ------------------------------------------

                if "my goals" in prompt_lower:
                    return (
                        f"Your performance goals are: "
                        f"{record.goals or 'Not provided'}"
                    )

                if "my strengths" in prompt_lower:
                    return (
                        f"Your performance strengths are: "
                        f"{record.strengths or 'Not provided'}"
                    )

                if "my weaknesses" in prompt_lower:
                    return (
                        f"Your performance weaknesses are: "
                        f"{record.weaknesses or 'Not provided'}"
                    )

                if "my feedback" in prompt_lower:
                    return (
                        f"Your performance feedback is: "
                        f"{record.feedback or 'Not provided'}"
                    )

                if "my reviewer" in prompt_lower:
                    return (
                        f"Your performance reviewer is: "
                        f"{record.reviewer or 'Not provided'}"
                    )

                if (
                    "my promotion" in prompt_lower
                    or "promotion status" in prompt_lower
                    or "eligible for promotion" in prompt_lower
                ):
                    return (
                        f"Your promotion status is: "
                        f"{record.promotion_status or 'Not Reviewed'}"
                    )

                if "my rating" in prompt_lower:
                    return (
                        f"Your latest performance rating is "
                        f"{record.rating}."
                    )

                return (
                    f"Performance for {employee.full_name}\n\n"
                    f"Employee ID: {employee.employee_id}\n"
                    f"Review Date: {record.review_date}\n"
                    f"Rating: {record.rating}\n"
                    f"Goals: {record.goals or 'Not provided'}\n"
                    f"Strengths: {record.strengths or 'Not provided'}\n"
                    f"Weaknesses: {record.weaknesses or 'Not provided'}\n"
                    f"Feedback: {record.feedback or 'Not provided'}\n"
                    f"Reviewer: {record.reviewer or 'Not provided'}\n"
                    f"Promotion Status: "
                    f"{record.promotion_status or 'Not Reviewed'}"
                )

            # ------------------------------------------
            # My Payroll / Salary
            # ------------------------------------------

            if (
                "my salary" in prompt_lower
                or "my deductions" in prompt_lower
                or "my payroll" in prompt_lower
            ):

                record = (
                    db.query(Payroll)
                    .filter(
                        Payroll.employee_id == employee.id
                    )
                    .order_by(
                        Payroll.pay_date.desc(),
                        Payroll.id.desc()
                    )
                    .first()
                )

                if not record:
                    return (
                        f"No payroll record found for "
                        f"{employee.full_name}."
                    )

                if "my deductions" in prompt_lower:
                    return (
                        f"Your deductions are "
                        f"{record.deductions}."
                    )

                if "my salary" in prompt_lower:
                    return (
                        f"Your net salary is "
                        f"{record.net_salary}."
                    )

                return (
                    f"Payroll for {employee.full_name}\n\n"
                    f"Basic Salary: {record.basic_salary}\n"
                    f"Bonus: {record.bonus}\n"
                    f"Allowances: {record.allowances}\n"
                    f"Deductions: {record.deductions}\n"
                    f"Net Salary: {record.net_salary}\n"
                    f"Pay Date: {record.pay_date or 'Not provided'}"
                )


        # ------------------------------------------
        # My Attendance
        # ------------------------------------------

        if "my attendance" in prompt_lower:

            record = (
                db.query(Attendance)
                .filter(
                    Attendance.employee_id == employee.id
                )
                .order_by(
                    Attendance.attendance_date.desc(),
                    Attendance.id.desc()
                )
                .first()
            )

            if not record:
                return (
                    f"No attendance record found for "
                    f"{employee.full_name}."
                )

            return (
                f"Attendance for {employee.full_name}\n\n"
                f"Employee ID: {employee.employee_id}\n"
                f"Date: {record.attendance_date}\n"
                f"Check In: "
                f"{record.check_in or 'Not recorded'}\n"
                f"Check Out: "
                f"{record.check_out or 'Not recorded'}\n"
                f"Status: {record.status}\n"
                f"Working Hours: "
                f"{record.working_hours}\n"
                f"Late Minutes: "
                f"{record.late_minutes}\n"
                f"Overtime Hours: "
                f"{record.overtime_hours}\n"
                f"Attendance Type: "
                f"{record.attendance_type}\n"
                f"Remarks: "
                f"{record.remarks or 'None'}"
            )

        # ------------------------------------------
        # My Leave
        # ------------------------------------------

        if (
            "my leave" in prompt_lower
            or "my leaves" in prompt_lower
        ):

            record = (
                db.query(LeaveRequest)
                .filter(
                    LeaveRequest.employee_id == employee.id
                )
                .order_by(
                    LeaveRequest.start_date.desc(),
                    LeaveRequest.id.desc()
                )
                .first()
            )

            if not record:
                return (
                    f"No leave record found for "
                    f"{employee.full_name}."
                )

            return (
                f"Leave Status for {employee.full_name}\n\n"
                f"Employee ID: {employee.employee_id}\n"
                f"Leave Type: {record.leave_type}\n"
                f"Start Date: {record.start_date}\n"
                f"End Date: {record.end_date}\n"
                f"Reason: "
                f"{record.reason or 'Not provided'}\n"
                f"Status: {record.status}"
            )

        # ------------------------------------------
        # My Onboarding
        # ------------------------------------------

        if "my onboarding" in prompt_lower:

            record = (
                db.query(Onboarding)
                .filter(
                    Onboarding.employee_id == employee.id
                )
                .order_by(
                    Onboarding.id.desc()
                )
                .first()
            )

            if not record:
                return (
                    f"No onboarding record found for "
                    f"{employee.full_name}."
                )

            return (
                f"Onboarding Status for {employee.full_name}\n\n"
                f"Employee ID: {employee.employee_id}\n"
                f"Status: {record.status}"
            )

        # ------------------------------------------
        # My Offboarding
        # ------------------------------------------

        if "my offboarding" in prompt_lower:

            record = (
                db.query(Offboarding)
                .filter(
                    Offboarding.employee_id == employee.id
                )
                .order_by(
                    Offboarding.id.desc()
                )
                .first()
            )

            if not record:
                return (
                    f"No offboarding record found for "
                    f"{employee.full_name}."
                )

            return (
                f"Offboarding Status for {employee.full_name}\n\n"
                f"Employee ID: {employee.employee_id}\n"
                f"Status: {record.status or 'Not provided'}\n"
                f"Resignation Date: "
                f"{record.resignation_date or 'Not provided'}\n"
                f"Last Working Day: "
                f"{record.last_working_day or 'Not provided'}\n"
                f"Exit Reason: "
                f"{record.exit_reason or 'Not provided'}"
            )


        # ==========================================
        # PRIORITY ADMIN ONBOARDING DATABASE AI
        # ==========================================
        # Handle onboarding questions before generic
        # AI/LLM routing can intercept them.

        if db is not None and employee_id is None and "onboarding" in prompt_lower:

            requested_employee = None

            # Detect employee name from the database.
            employees = db.query(Employee).all()

            for candidate in employees:
                candidate_name = candidate.full_name.lower().strip()

                if candidate_name and candidate_name in prompt_lower:
                    requested_employee = candidate
                    break

            # Detect onboarding status.
            requested_status = None

            if "completed" in prompt_lower:
                requested_status = "Completed"
            elif "in progress" in prompt_lower:
                requested_status = "In Progress"
            elif "pending" in prompt_lower:
                requested_status = "Pending"

            query = (
                db.query(Onboarding, Employee)
                .join(
                    Employee,
                    Onboarding.employee_id == Employee.id
                )
            )

            if requested_employee:
                query = query.filter(
                    Onboarding.employee_id == requested_employee.id
                )

            if requested_status:
                query = query.filter(
                    func.lower(Onboarding.status)
                    == requested_status.lower()
                )

            records = (
                query
                .order_by(Onboarding.id.desc())
                .all()
            )

            if not records:

                if requested_employee and requested_status:
                    return (
                        f"No {requested_status.lower()} onboarding "
                        f"record found for {requested_employee.full_name}."
                    )

                if requested_employee:
                    return (
                        f"No onboarding record found for "
                        f"{requested_employee.full_name}."
                    )

                if requested_status:
                    return (
                        f"No {requested_status.lower()} onboarding "
                        f"records found."
                    )

                return "No onboarding records found in the database."

            if requested_employee:
                lines = [
                    f"Onboarding for {requested_employee.full_name}:",
                    ""
                ]
            elif requested_status:
                lines = [
                    f"{requested_status} Onboarding Records:",
                    ""
                ]
            else:
                lines = [
                    "Onboarding records found in the database:",
                    ""
                ]

            for record, employee in records:

                lines.extend([
                    f"Employee ID: {employee.employee_id}",
                    f"Name: {employee.full_name}",
                    f"Offer Status: {record.offer_status or 'Not provided'}",
                    f"Documents Uploaded: {'Yes' if record.documents_uploaded else 'No'}",
                    f"Email Created: {'Yes' if record.email_created else 'No'}",
                    f"ID Card Issued: {'Yes' if record.id_card_issued else 'No'}",
                    f"Laptop Assigned: {'Yes' if record.laptop_assigned else 'No'}",
                    f"Orientation Completed: {'Yes' if record.orientation_completed else 'No'}",
                    f"Manager Assigned: {'Yes' if record.manager_assigned else 'No'}",
                    f"Status: {record.status or 'In Progress'}",
                    f"Joining Date: {record.joining_date or 'Not provided'}",
                    f"Mentor: {record.mentor or 'Not assigned'}",
                    f"Training Status: {record.training_status or 'Not provided'}",
                    f"Welcome Kit: {record.welcome_kit or 'Not provided'}",
                    "-" * 45
                ])

            return "\n".join(lines)


        # ==========================================
        # ADMIN DATABASE AI
        # ==========================================
        #
        # Admin users call AIService with employee_id=None.
        # These branches therefore query the complete database.
        #

        admin_list_request = any(
            phrase in prompt_lower
            for phrase in [
                "show all",
                "list all",
                "show every",
                "list every",
                "all employees",
                "all departments",
                "all attendance",
                "all leave",
                "all payroll",
                "all performances",
                "all performance",
                "all onboarding",
                "all offboarding"
            ]
        )

        if db is not None and employee_id is None and admin_list_request:

            # ==========================================
            # ALL EMPLOYEES
            # ==========================================

            if any(
                phrase in prompt_lower
                for phrase in [
                    "employee",
                    "employees"
                ]
            ) and not any(
                phrase in prompt_lower
                for phrase in [
                    "attendance",
                    "leave",
                    "payroll",
                    "performance",
                    "onboarding",
                    "offboarding"
                ]
            ):

                employees = (
                    db.query(Employee)
                    .order_by(Employee.id)
                    .all()
                )

                if not employees:
                    return "No employees found in the database."

                lines = ["Employees found in the database:", ""]

                for employee in employees:

                    department_name = (
                        employee.department.department_name
                        if employee.department
                        else "Not assigned"
                    )

                    lines.extend([
                        f"Employee ID: {employee.employee_id}",
                        f"Name: {employee.full_name}",
                        f"Email: {employee.email}",
                        f"Department: {department_name}",
                        f"Designation: {employee.designation or 'Not provided'}",
                        f"Salary: {employee.salary if employee.salary is not None else 'Not provided'}",
                        f"Phone: {employee.phone or 'Not provided'}",
                        f"Address: {employee.address or 'Not provided'}",
                        f"Joining Date: {employee.joining_date or 'Not provided'}",
                        f"Date of Birth: {employee.date_of_birth or 'Not provided'}",
                        f"Nationality: {employee.nationality or 'Not provided'}",
                        f"Emergency Contact: {employee.emergency_contact or 'Not provided'}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ==========================================
            # ALL DEPARTMENTS
            # ==========================================

            if "department" in prompt_lower:

                departments = (
                    db.query(Department)
                    .order_by(Department.id)
                    .all()
                )

                if not departments:
                    return "No departments found in the database."

                lines = [
                    "Departments found in the database:",
                    ""
                ]

                for department in departments:

                    employee_count = (
                        db.query(Employee)
                        .filter(
                            Employee.department_id == department.id
                        )
                        .count()
                    )

                    lines.extend([
                        f"Department ID: {department.id}",
                        f"Department: {department.department_name}",
                        f"Description: {department.description or 'Not provided'}",
                        f"Employees: {employee_count}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ==========================================
            # ALL ATTENDANCE
            # ==========================================

            if "attendance" in prompt_lower:

                records = (
                    db.query(Attendance)
                    .order_by(
                        Attendance.attendance_date.desc(),
                        Attendance.id.desc()
                    )
                    .all()
                )

                if not records:
                    return "No attendance records found in the database."

                lines = [
                    "Attendance records found in the database:",
                    ""
                ]

                for record in records:

                    employee_name = (
                        record.employee.full_name
                        if record.employee
                        else "Unknown employee"
                    )

                    employee_code = (
                        record.employee.employee_id
                        if record.employee
                        else "Unknown"
                    )

                    lines.extend([
                        f"Employee ID: {employee_code}",
                        f"Name: {employee_name}",
                        f"Date: {record.attendance_date}",
                        f"Check In: {record.check_in or 'Not recorded'}",
                        f"Check Out: {record.check_out or 'Not recorded'}",
                        f"Status: {record.status or 'Not provided'}",
                        f"Working Hours: {record.working_hours}",
                        f"Late Minutes: {record.late_minutes}",
                        f"Overtime Hours: {record.overtime_hours}",
                        f"Attendance Type: {record.attendance_type or 'Regular'}",
                        f"Remarks: {record.remarks or 'None'}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ==========================================
            # ALL LEAVE
            # ==========================================

            if "leave" in prompt_lower:

                records = (
                    db.query(LeaveRequest)
                    .order_by(
                        LeaveRequest.start_date.desc(),
                        LeaveRequest.id.desc()
                    )
                    .all()
                )

                if not records:
                    return "No leave records found in the database."

                lines = [
                    "Leave records found in the database:",
                    ""
                ]

                for record in records:

                    employee_name = (
                        record.employee.full_name
                        if record.employee
                        else "Unknown employee"
                    )

                    employee_code = (
                        record.employee.employee_id
                        if record.employee
                        else "Unknown"
                    )

                    lines.extend([
                        f"Employee ID: {employee_code}",
                        f"Name: {employee_name}",
                        f"Leave Type: {record.leave_type}",
                        f"Start Date: {record.start_date}",
                        f"End Date: {record.end_date}",
                        f"Reason: {record.reason or 'Not provided'}",
                        f"Status: {record.status or 'Pending'}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ==========================================
            # ALL PAYROLL
            # ==========================================

            if "payroll" in prompt_lower:

                records = (
                    db.query(Payroll)
                    .order_by(
                        Payroll.pay_date.desc(),
                        Payroll.id.desc()
                    )
                    .all()
                )

                if not records:
                    return "No payroll records found in the database."

                lines = [
                    "Payroll records found in the database:",
                    ""
                ]

                for record in records:

                    employee_name = (
                        record.employee.full_name
                        if record.employee
                        else "Unknown employee"
                    )

                    employee_code = (
                        record.employee.employee_id
                        if record.employee
                        else "Unknown"
                    )

                    lines.extend([
                        f"Employee ID: {employee_code}",
                        f"Name: {employee_name}",
                        f"Basic Salary: {record.basic_salary}",
                        f"Bonus: {record.bonus}",
                        f"Allowances: {record.allowances}",
                        f"Deductions: {record.deductions}",
                        f"Net Salary: {record.net_salary}",
                        f"Pay Date: {record.pay_date or 'Not provided'}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ==========================================
            # ALL PERFORMANCE
            # ==========================================

            if "performance" in prompt_lower:

                records = (
                    db.query(Performance)
                    .order_by(
                        Performance.review_date.desc(),
                        Performance.id.desc()
                    )
                    .all()
                )

                if not records:
                    return "No performance records found in the database."

                lines = [
                    "Performance records found in the database:",
                    ""
                ]

                for record in records:

                    employee_name = (
                        record.employee.full_name
                        if record.employee
                        else "Unknown employee"
                    )

                    employee_code = (
                        record.employee.employee_id
                        if record.employee
                        else "Unknown"
                    )

                    lines.extend([
                        f"Employee ID: {employee_code}",
                        f"Name: {employee_name}",
                        f"Review Date: {record.review_date}",
                        f"Rating: {record.rating}",
                        f"Goals: {record.goals or 'Not provided'}",
                        f"Strengths: {record.strengths or 'Not provided'}",
                        f"Weaknesses: {record.weaknesses or 'Not provided'}",
                        f"Feedback: {record.feedback or 'Not provided'}",
                        f"Reviewer: {record.reviewer}",
                        f"Promotion Status: {record.promotion_status or 'Not Reviewed'}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ==========================================
            # ONBOARDING DATABASE AI
            # ==========================================
            # Handles real onboarding database queries.
            #
            # Examples:
            #   show all onboarding
            #   show Shyam onboarding
            #   show onboarding for Shyam
            #   show pending onboarding
            #   show completed onboarding

            if (
                "onboarding" in prompt_lower
                and db is not None
            ):

                # ------------------------------------------
                # Detect employee
                # ------------------------------------------

                requested_employee = None

                employees = db.query(Employee).all()

                for candidate in employees:
                    candidate_name = (
                        candidate.full_name.lower().strip()
                    )

                    if (
                        candidate_name
                        and candidate_name in prompt_lower
                    ):
                        requested_employee = candidate
                        break

                # ------------------------------------------
                # Detect onboarding status
                # ------------------------------------------

                requested_status = None

                if "completed" in prompt_lower:
                    requested_status = "Completed"
                elif "in progress" in prompt_lower:
                    requested_status = "In Progress"
                elif "pending" in prompt_lower:
                    requested_status = "Pending"

                # ------------------------------------------
                # Build database query
                # ------------------------------------------

                query = (
                    db.query(Onboarding, Employee)
                    .join(
                        Employee,
                        Onboarding.employee_id == Employee.id
                    )
                )

                if requested_employee:
                    query = query.filter(
                        Onboarding.employee_id
                        == requested_employee.id
                    )

                if requested_status:
                    query = query.filter(
                        func.lower(Onboarding.status)
                        == requested_status.lower()
                    )

                records = (
                    query
                    .order_by(Onboarding.id.desc())
                    .all()
                )

                # ------------------------------------------
                # No records
                # ------------------------------------------

                if not records:

                    if requested_employee and requested_status:
                        return (
                            f"No {requested_status.lower()} onboarding "
                            f"record found for "
                            f"{requested_employee.full_name}."
                        )

                    if requested_employee:
                        return (
                            f"No onboarding record found for "
                            f"{requested_employee.full_name}."
                        )

                    if requested_status:
                        return (
                            f"No {requested_status.lower()} onboarding "
                            f"records found."
                        )

                    return (
                        "No onboarding records found "
                        "in the database."
                    )

                # ------------------------------------------
                # Response heading
                # ------------------------------------------

                if requested_employee:
                    lines = [
                        f"Onboarding for "
                        f"{requested_employee.full_name}:",
                        ""
                    ]

                elif requested_status:
                    lines = [
                        f"{requested_status} Onboarding Records:",
                        ""
                    ]

                else:
                    lines = [
                        "Onboarding records found in the database:",
                        ""
                    ]

                # ------------------------------------------
                # Format database records
                # ------------------------------------------

                for record, employee in records:

                    lines.extend([
                        f"Employee ID: {employee.employee_id}",
                        f"Name: {employee.full_name}",
                        f"Offer Status: "
                        f"{record.offer_status or 'Not provided'}",
                        f"Documents Uploaded: "
                        f"{'Yes' if record.documents_uploaded else 'No'}",
                        f"Email Created: "
                        f"{'Yes' if record.email_created else 'No'}",
                        f"ID Card Issued: "
                        f"{'Yes' if record.id_card_issued else 'No'}",
                        f"Laptop Assigned: "
                        f"{'Yes' if record.laptop_assigned else 'No'}",
                        f"Orientation Completed: "
                        f"{'Yes' if record.orientation_completed else 'No'}",
                        f"Manager Assigned: "
                        f"{'Yes' if record.manager_assigned else 'No'}",
                        f"Status: "
                        f"{record.status or 'In Progress'}",
                        f"Joining Date: "
                        f"{record.joining_date or 'Not provided'}",
                        f"Mentor: "
                        f"{record.mentor or 'Not assigned'}",
                        f"Training Status: "
                        f"{record.training_status or 'Not provided'}",
                        f"Welcome Kit: "
                        f"{record.welcome_kit or 'Not provided'}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ==========================================
            # ALL ONBOARDING
            # ==========================================

            if "onboarding" in prompt_lower:

                records = (
                    db.query(Onboarding)
                    .order_by(Onboarding.id)
                    .all()
                )

                if not records:
                    return "No onboarding records found in the database."

                lines = [
                    "Onboarding records found in the database:",
                    ""
                ]

                for record in records:

                    employee_name = (
                        record.employee.full_name
                        if record.employee
                        else "Unknown employee"
                    )

                    employee_code = (
                        record.employee.employee_id
                        if record.employee
                        else "Unknown"
                    )

                    lines.extend([
                        f"Employee ID: {employee_code}",
                        f"Name: {employee_name}",
                        f"Offer Status: {record.offer_status}",
                        f"Documents Uploaded: {record.documents_uploaded}",
                        f"Email Created: {record.email_created}",
                        f"ID Card Issued: {record.id_card_issued}",
                        f"Laptop Assigned: {record.laptop_assigned}",
                        f"Orientation Completed: {record.orientation_completed}",
                        f"Manager Assigned: {record.manager_assigned}",
                        f"Status: {record.status}",
                        f"Joining Date: {record.joining_date or 'Not provided'}",
                        f"Mentor: {record.mentor or 'Not assigned'}",
                        f"Training Status: {record.training_status or 'Not provided'}",
                        f"Welcome Kit: {record.welcome_kit or 'Not provided'}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ==========================================
            # ALL OFFBOARDING
            # ==========================================

            if "offboarding" in prompt_lower:

                records = (
                    db.query(Offboarding)
                    .order_by(Offboarding.id)
                    .all()
                )

                if not records:
                    return "No offboarding records found in the database."

                lines = [
                    "Offboarding records found in the database:",
                    ""
                ]

                for record in records:

                    employee_name = (
                        record.employee.full_name
                        if record.employee
                        else "Unknown employee"
                    )

                    employee_code = (
                        record.employee.employee_id
                        if record.employee
                        else "Unknown"
                    )

                    lines.extend([
                        f"Employee ID: {employee_code}",
                        f"Name: {employee_name}",
                        f"Resignation Date: {record.resignation_date or 'Not provided'}",
                        f"Last Working Day: {record.last_working_day or 'Not provided'}",
                        f"Exit Reason: {record.exit_reason or 'Not provided'}",
                        f"Laptop Returned: {record.laptop_returned}",
                        f"ID Card Returned: {record.id_card_returned}",
                        f"Account Disabled: {record.account_disabled}",
                        f"Exit Interview Completed: {record.exit_interview_completed}",
                        f"Final Settlement Completed: {record.final_settlement_completed}",
                        f"Status: {record.status}",
                        "-" * 45
                    ])

                return "\n".join(lines)

        # ==========================================
        # ADMIN ANALYTICAL DATABASE AI
        # ==========================================
        # Handles questions that require calculation,
        # filtering, ranking, or comparison across employees.

        if db is not None and employee_id is None:

            # Highest salary
            if (
                "highest salary" in prompt_lower
                or "maximum salary" in prompt_lower
                or "max salary" in prompt_lower
                or "who earns the most" in prompt_lower
            ):
                employee = (
                    db.query(Employee)
                    .order_by(Employee.salary.desc())
                    .first()
                )

                if not employee:
                    return "No employees found."

                return (
                    "Highest Salary Employee\n\n"
                    f"Name: {employee.full_name}\n"
                    f"Employee ID: {employee.employee_id}\n"
                    f"Designation: {employee.designation}\n"
                    f"Salary: {employee.salary}"
                )

            # Lowest salary
            if (
                "lowest salary" in prompt_lower
                or "minimum salary" in prompt_lower
                or "min salary" in prompt_lower
                or "who earns the least" in prompt_lower
            ):
                employee = (
                    db.query(Employee)
                    .order_by(Employee.salary.asc())
                    .first()
                )

                if not employee:
                    return "No employees found."

                return (
                    "Lowest Salary Employee\n\n"
                    f"Name: {employee.full_name}\n"
                    f"Employee ID: {employee.employee_id}\n"
                    f"Designation: {employee.designation}\n"
                    f"Salary: {employee.salary}"
                )

            # Total payroll
            if (
                "total payroll" in prompt_lower
                or "payroll total" in prompt_lower
                or "total payroll amount" in prompt_lower
            ):
                total = (
                    db.query(
                        func.coalesce(
                            func.sum(Payroll.net_salary),
                            0
                        )
                    )
                    .scalar()
                )

                return (
                    "Total Payroll\n\n"
                    f"Total Net Payroll: {total}"
                )

            # Currently on leave
            if (
                "currently on leave" in prompt_lower
                or "who is on leave" in prompt_lower
                or "employees on leave" in prompt_lower
            ):
                today = date.today()

                records = (
                    db.query(LeaveRequest, Employee)
                    .join(
                        Employee,
                        LeaveRequest.employee_id == Employee.id
                    )
                    .filter(
                        func.lower(LeaveRequest.status) == "approved",
                        LeaveRequest.start_date <= today,
                        LeaveRequest.end_date >= today
                    )
                    .all()
                )

                if not records:
                    return "No employees are currently on approved leave."

                lines = [
                    "Employees Currently on Leave:",
                    ""
                ]

                for leave, employee in records:
                    lines.extend([
                        f"Name: {employee.full_name}",
                        f"Employee ID: {employee.employee_id}",
                        f"Leave Type: {leave.leave_type}",
                        f"Start Date: {leave.start_date}",
                        f"End Date: {leave.end_date}",
                        f"Status: {leave.status}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # Late attendance by date
            if (
                "late today" in prompt_lower
                or "who was late today" in prompt_lower
                or "employees who were late today" in prompt_lower
                or "late yesterday" in prompt_lower
                or "who was late yesterday" in prompt_lower
                or "employees who were late yesterday" in prompt_lower
            ):
                if "yesterday" in prompt_lower:
                    requested_late_date = date.today() - timedelta(days=1)
                    date_label = "Yesterday"
                else:
                    requested_late_date = date.today()
                    date_label = "Today"

                records = (
                    db.query(Attendance, Employee)
                    .join(
                        Employee,
                        Attendance.employee_id == Employee.id
                    )
                    .filter(
                        Attendance.attendance_date == requested_late_date,
                        func.lower(Attendance.status) == "late"
                    )
                    .order_by(Attendance.id.desc())
                    .all()
                )

                if not records:
                    return (
                        f"No employees were marked late on "
                        f"{requested_late_date.strftime('%d-%m-%Y')}."
                    )

                lines = [
                    f"Employees Late {date_label} "
                    f"({requested_late_date.strftime('%d-%m-%Y')}):",
                    ""
                ]

                for attendance, employee in records:
                    lines.extend([
                        f"Name: {employee.full_name}",
                        f"Employee ID: {employee.employee_id}",
                        f"Check In: {attendance.check_in or 'Not recorded'}",
                        f"Late Minutes: {attendance.late_minutes}",
                        f"Status: {attendance.status}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # Best performance
            if (
                "best performance rating" in prompt_lower
                or "highest performance rating" in prompt_lower
                or "best performance" in prompt_lower
                or "highest performance" in prompt_lower
            ):
                record = (
                    db.query(Performance, Employee)
                    .join(
                        Employee,
                        Performance.employee_id == Employee.id
                    )
                    .order_by(
                        Performance.rating.desc(),
                        Performance.review_date.desc()
                    )
                    .first()
                )

                if not record:
                    return "No performance records found."

                performance, employee = record

                return (
                    "Best Performance\n\n"
                    f"Name: {employee.full_name}\n"
                    f"Employee ID: {employee.employee_id}\n"
                    f"Rating: {performance.rating}\n"
                    f"Review Date: {performance.review_date}\n"
                    f"Promotion Status: {performance.promotion_status}"
                )

            # Promotion eligibility
            if (
                "eligible for promotion" in prompt_lower
                or "promotion eligible" in prompt_lower
            ):
                records = (
                    db.query(Performance, Employee)
                    .join(
                        Employee,
                        Performance.employee_id == Employee.id
                    )
                    .filter(
                        func.lower(
                            Performance.promotion_status
                        ) == "eligible"
                    )
                    .order_by(Performance.rating.desc())
                    .all()
                )

                if not records:
                    return "No employees are currently marked as eligible for promotion."

                lines = [
                    "Employees Eligible for Promotion:",
                    ""
                ]

                for performance, employee in records:
                    lines.extend([
                        f"Name: {employee.full_name}",
                        f"Employee ID: {employee.employee_id}",
                        f"Rating: {performance.rating}",
                        f"Review Date: {performance.review_date}",
                        f"Promotion Status: {performance.promotion_status}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # Pending leave requests
            if (
                "pending leave requests" in prompt_lower
                or "pending leave" in prompt_lower
                or "who has pending leave" in prompt_lower
            ):
                records = (
                    db.query(LeaveRequest, Employee)
                    .join(
                        Employee,
                        LeaveRequest.employee_id == Employee.id
                    )
                    .filter(
                        func.lower(LeaveRequest.status) == "pending"
                    )
                    .all()
                )

                if not records:
                    return "There are no pending leave requests."

                lines = [
                    "Pending Leave Requests:",
                    ""
                ]

                for leave, employee in records:
                    lines.extend([
                        f"Name: {employee.full_name}",
                        f"Employee ID: {employee.employee_id}",
                        f"Leave Type: {leave.leave_type}",
                        f"Start Date: {leave.start_date}",
                        f"End Date: {leave.end_date}",
                        f"Reason: {leave.reason or 'Not provided'}",
                        f"Status: {leave.status}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # Employee count
            if (
                "how many employees" in prompt_lower
                or "employee count" in prompt_lower
                or "total employees" in prompt_lower
            ):
                count = db.query(Employee).count()

                return (
                    "Employee Count\n\n"
                    f"Total Employees: {count}"
                )

        # ==========================================
        # DATE-SPECIFIC ATTENDANCE / LEAVE AI
        # ==========================================
        # Supports:
        # today / today's
        # yesterday / yesterday's
        # specific dates: YYYY-MM-DD or DD/MM/YYYY
        # optional employee name, e.g.:
        # "show Shyam yesterday attendance"

        if db is not None and employee_id is None:

            from datetime import datetime

            requested_date = None

            # -------------------------------
            # Detect relative dates
            # -------------------------------

            if (
                "today" in prompt_lower
                or "today's" in prompt_lower
                or "todays" in prompt_lower
            ):
                requested_date = date.today()

            elif (
                "yesterday" in prompt_lower
                or "yesterday's" in prompt_lower
                or "yesterdays" in prompt_lower
            ):
                requested_date = date.today() - timedelta(days=1)

            # -------------------------------
            # Detect YYYY-MM-DD
            # -------------------------------

            if requested_date is None:
                match = re.search(
                    r"\b(20\d{2})-(\d{1,2})-(\d{1,2})\b",
                    prompt_lower
                )

                if match:
                    try:
                        requested_date = date(
                            int(match.group(1)),
                            int(match.group(2)),
                            int(match.group(3))
                        )
                    except ValueError:
                        requested_date = None

            # -------------------------------
            # Detect DD/MM/YYYY
            # -------------------------------

            if requested_date is None:
                match = re.search(
                    r"\b(\d{1,2})/(\d{1,2})/(20\d{2})\b",
                    prompt_lower
                )

                if match:
                    try:
                        requested_date = date(
                            int(match.group(3)),
                            int(match.group(2)),
                            int(match.group(1))
                        )
                    except ValueError:
                        requested_date = None

            # -------------------------------
            # Only process date-specific
            # attendance / leave requests
            # -------------------------------

            if requested_date is not None and (
                "attendance" in prompt_lower
                or "leave" in prompt_lower
                or "leaves" in prompt_lower
            ):

                # --------------------------------
                # Try to detect employee name
                # --------------------------------

                requested_employee = None

                employees = db.query(Employee).all()

                for candidate in employees:
                    candidate_name = (
                        candidate.full_name.lower().strip()
                    )

                    if (
                        candidate_name
                        and candidate_name in prompt_lower
                    ):
                        requested_employee = candidate
                        break

                # =================================
                # ATTENDANCE
                # =================================

                if "attendance" in prompt_lower:

                    query = (
                        db.query(Attendance, Employee)
                        .join(
                            Employee,
                            Attendance.employee_id == Employee.id
                        )
                        .filter(
                            Attendance.attendance_date
                            == requested_date
                        )
                    )

                    if requested_employee:
                        query = query.filter(
                            Attendance.employee_id
                            == requested_employee.id
                        )

                    records = (
                        query
                        .order_by(Attendance.id.desc())
                        .all()
                    )

                    date_label = requested_date.strftime(
                        "%d-%m-%Y"
                    )

                    if not records:
                        if requested_employee:
                            return (
                                f"No attendance records found for "
                                f"{requested_employee.full_name} "
                                f"on {date_label}."
                            )

                        return (
                            f"No attendance records found for "
                            f"{date_label}."
                        )

                    lines = [
                        f"Attendance for {date_label}:",
                        ""
                    ]

                    for attendance, employee in records:
                        lines.extend([
                            f"Name: {employee.full_name}",
                            f"Employee ID: {employee.employee_id}",
                            f"Date: {attendance.attendance_date}",
                            f"Check In: "
                            f"{attendance.check_in or 'Not recorded'}",
                            f"Check Out: "
                            f"{attendance.check_out or 'Not recorded'}",
                            f"Status: {attendance.status}",
                            f"Working Hours: "
                            f"{attendance.working_hours}",
                            f"Late Minutes: "
                            f"{attendance.late_minutes}",
                            f"Overtime Hours: "
                            f"{attendance.overtime_hours}",
                            f"Attendance Type: "
                            f"{attendance.attendance_type}",
                            f"Remarks: "
                            f"{attendance.remarks or 'None'}",
                            "-" * 45
                        ])

                    return "\n".join(lines)

                # =================================
                # LEAVE
                # =================================

                if "leave" in prompt_lower or "leaves" in prompt_lower:

                    query = (
                        db.query(LeaveRequest, Employee)
                        .join(
                            Employee,
                            LeaveRequest.employee_id == Employee.id
                        )
                        .filter(
                            LeaveRequest.start_date
                            <= requested_date,
                            LeaveRequest.end_date
                            >= requested_date
                        )
                    )

                    if requested_employee:
                        query = query.filter(
                            LeaveRequest.employee_id
                            == requested_employee.id
                        )

                    records = (
                        query
                        .order_by(LeaveRequest.id.desc())
                        .all()
                    )

                    date_label = requested_date.strftime(
                        "%d-%m-%Y"
                    )

                    if not records:
                        if requested_employee:
                            return (
                                f"No leave records found for "
                                f"{requested_employee.full_name} "
                                f"on {date_label}."
                            )

                        return (
                            f"No employee leave records found for "
                            f"{date_label}."
                        )

                    lines = [
                        f"Employee Leaves for {date_label}:",
                        ""
                    ]

                    for leave, employee in records:
                        lines.extend([
                            f"Name: {employee.full_name}",
                            f"Employee ID: {employee.employee_id}",
                            f"Leave Type: {leave.leave_type}",
                            f"Start Date: {leave.start_date}",
                            f"End Date: {leave.end_date}",
                            f"Reason: "
                            f"{leave.reason or 'Not provided'}",
                            f"Status: {leave.status}",
                            "-" * 45
                        ])

                    return "\n".join(lines)

        # ==========================================
        # ADMIN EMPLOYEE-SPECIFIC DATABASE AI
        # ==========================================
        # Handles questions about a particular employee.
        # Example:
        # "What is Meghana's payroll?"
        # "What is Meghana's performance?"
        # "What is Meghana's leave status?"
        # "What is Meghana's attendance?"

        if db is not None and employee_id is None:

            # ------------------------------------------
            # Salary threshold
            # ------------------------------------------


            salary_match = re.search(
                r"salary\s+(above|over|greater than|below|under|less than)\s+([0-9]+(?:\.[0-9]+)?)",
                prompt_lower
            )

            if salary_match:

                operator = salary_match.group(1)
                threshold = float(salary_match.group(2))

                if operator in ("above", "over", "greater than"):
                    employees = (
                        db.query(Employee)
                        .filter(Employee.salary > threshold)
                        .order_by(Employee.salary.desc())
                        .all()
                    )
                    title = f"Employees With Salary Above {threshold}"

                else:
                    employees = (
                        db.query(Employee)
                        .filter(Employee.salary < threshold)
                        .order_by(Employee.salary.asc())
                        .all()
                    )
                    title = f"Employees With Salary Below {threshold}"

                if not employees:
                    return (
                        f"No employees have a salary "
                        f"{'above' if operator in ('above', 'over', 'greater than') else 'below'} "
                        f"{threshold}."
                    )

                lines = [
                    title + ":",
                    ""
                ]

                for employee in employees:
                    lines.extend([
                        f"Name: {employee.full_name}",
                        f"Employee ID: {employee.employee_id}",
                        f"Designation: {employee.designation}",
                        f"Salary: {employee.salary}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ------------------------------------------
            # Find employee by name
            # ------------------------------------------

            employee = None

            # Find the employee mentioned in the question.
            #
            # Matching priority:
            # 1. Exact full name
            # 2. Name with spaces removed
            # 3. Full name contained in the question
            #
            # Candidates are checked by longest name first so that
            # "Vishnu Priya" is selected before "Vishnu".

            employees = db.query(Employee).all()

            def normalize_name(value):
                return re.sub(r"[^a-z0-9]", "", value.lower())

            # Remove common question words before matching.
            searchable_prompt = prompt_lower

            normalized_prompt = normalize_name(searchable_prompt)

            # Longest names first prevents "vishnu" from winning
            # when the user actually means "vishnu priya".
            employees = sorted(
                employees,
                key=lambda candidate: len(
                    normalize_name(candidate.full_name or "")
                ),
                reverse=True
            )

            for candidate in employees:

                name = (candidate.full_name or "").strip()

                if not name:
                    continue

                name_lower = name.lower()
                normalized_name = normalize_name(name)

                # Exact full name in the original question.
                if name_lower in searchable_prompt:
                    employee = candidate
                    break

                # Allow "vishnupriya" to match "Vishnu Priya".
                if normalized_name and normalized_name in normalized_prompt:
                    employee = candidate
                    break

            if employee:

                # --------------------------------------
                # Employee attendance
                # --------------------------------------

                if "attendance" in prompt_lower:

                    records = (
                        db.query(Attendance)
                        .filter(
                            Attendance.employee_id == employee.id
                        )
                        .order_by(
                            Attendance.attendance_date.desc()
                        )
                        .all()
                    )

                    if not records:
                        return (
                            f"No attendance records found for "
                            f"{employee.full_name}."
                        )

                    lines = [
                        f"Attendance for {employee.full_name}:",
                        ""
                    ]

                    for record in records:
                        lines.extend([
                            f"Date: {record.attendance_date}",
                            f"Check In: {record.check_in or 'Not recorded'}",
                            f"Check Out: {record.check_out or 'Not recorded'}",
                            f"Status: {record.status}",
                            f"Working Hours: {record.working_hours}",
                            f"Late Minutes: {record.late_minutes}",
                            f"Overtime Hours: {record.overtime_hours}",
                            f"Attendance Type: {record.attendance_type}",
                            f"Remarks: {record.remarks or 'None'}",
                            "-" * 45
                        ])

                    return "\n".join(lines)

                # --------------------------------------
                # Employee payroll
                # --------------------------------------

                if (
                    "payroll" in prompt_lower
                    or "salary" in prompt_lower
                    or "pay" in prompt_lower
                    or "bonus" in prompt_lower
                    or "allowances" in prompt_lower
                    or "allowance" in prompt_lower
                    or "deductions" in prompt_lower
                    or "deduction" in prompt_lower
                    or "basic salary" in prompt_lower
                    or "net salary" in prompt_lower
                ):

                    record = (
                        db.query(Payroll)
                        .filter(
                            Payroll.employee_id == employee.id
                        )
                        .order_by(
                            Payroll.pay_date.desc(),
                            Payroll.id.desc()
                        )
                        .first()
                    )

                    if not record:
                        return (
                            f"No payroll record found for "
                            f"{employee.full_name}."
                        )

                    return (
                        f"Payroll for {employee.full_name}\n\n"
                        f"Employee ID: {employee.employee_id}\n"
                        f"Basic Salary: {record.basic_salary}\n"
                        f"Bonus: {record.bonus}\n"
                        f"Allowances: {record.allowances}\n"
                        f"Deductions: {record.deductions}\n"
                        f"Net Salary: {record.net_salary}\n"
                        f"Pay Date: {record.pay_date or 'Not provided'}"
                    )

                # --------------------------------------
                # Employee performance
                # --------------------------------------

                if "performance" in prompt_lower:

                    record = (
                        db.query(Performance)
                        .filter(
                            Performance.employee_id == employee.id
                        )
                        .order_by(
                            Performance.review_date.desc(),
                            Performance.id.desc()
                        )
                        .first()
                    )

                    if not record:
                        return (
                            f"No performance record found for "
                            f"{employee.full_name}."
                        )

                    return (
                        f"Performance for {employee.full_name}\n\n"
                        f"Employee ID: {employee.employee_id}\n"
                        f"Review Date: {record.review_date}\n"
                        f"Rating: {record.rating}\n"
                        f"Goals: {record.goals or 'Not provided'}\n"
                        f"Strengths: {record.strengths or 'Not provided'}\n"
                        f"Weaknesses: {record.weaknesses or 'Not provided'}\n"
                        f"Feedback: {record.feedback or 'Not provided'}\n"
                        f"Reviewer: {record.reviewer}\n"
                        f"Promotion Status: "
                        f"{record.promotion_status or 'Not Reviewed'}"
                    )

                # --------------------------------------
                # Employee offboarding
                # --------------------------------------

                if "offboarding" in prompt_lower:

                    record = (
                        db.query(Offboarding)
                        .filter(
                            Offboarding.employee_id == employee.id
                        )
                        .order_by(
                            Offboarding.id.desc()
                        )
                        .first()
                    )

                    if not record:
                        return (
                            f"No offboarding record found for "
                            f"{employee.full_name}."
                        )

                    return (
                        f"Offboarding for {employee.full_name}\n\n"
                        f"Employee ID: {employee.employee_id}\n"
                        f"Resignation Date: "
                        f"{record.resignation_date or 'Not provided'}\n"
                        f"Last Working Day: "
                        f"{record.last_working_day or 'Not provided'}\n"
                        f"Exit Reason: "
                        f"{record.exit_reason or 'Not provided'}\n"
                        f"Laptop Returned: "
                        f"{'Yes' if record.laptop_returned else 'No'}\n"
                        f"ID Card Returned: "
                        f"{'Yes' if record.id_card_returned else 'No'}\n"
                        f"Account Disabled: "
                        f"{'Yes' if record.account_disabled else 'No'}\n"
                        f"Exit Interview Completed: "
                        f"{'Yes' if record.exit_interview_completed else 'No'}\n"
                        f"Final Settlement Completed: "
                        f"{'Yes' if record.final_settlement_completed else 'No'}\n"
                        f"Status: "
                        f"{record.status or 'Not provided'}"
                    )

                # --------------------------------------
                # Employee leave
                # --------------------------------------

                if "leave" in prompt_lower:

                    records = (
                        db.query(LeaveRequest)
                        .filter(
                            LeaveRequest.employee_id == employee.id
                        )
                        .order_by(
                            LeaveRequest.start_date.desc()
                        )
                        .all()
                    )

                    if not records:
                        return (
                            f"No leave records found for "
                            f"{employee.full_name}."
                        )

                    lines = [
                        f"Leave Status for {employee.full_name}:",
                        ""
                    ]

                    for record in records:
                        lines.extend([
                            f"Leave Type: {record.leave_type}",
                            f"Start Date: {record.start_date}",
                            f"End Date: {record.end_date}",
                            f"Reason: {record.reason or 'Not provided'}",
                            f"Status: {record.status}",
                            "-" * 45
                        ])

                    return "\n".join(lines)

        # ==========================================
        # DOCUMENT DATABASE AI
        # ==========================================
        # Handles real EmployeeDocument database queries.
        #
        # Examples:
        #   show all documents
        #   show documents for harshita
        #   show harshita documents
        #   show approved documents
        #   show pending documents
        #   show rejected documents

        if db is not None and (
            "document" in prompt_lower
            or "documents" in prompt_lower
        ):

            # ------------------------------------------
            # Detect document status
            # ------------------------------------------

            document_status = None

            if "approved" in prompt_lower:
                document_status = "Approved"
            elif "rejected" in prompt_lower:
                document_status = "Rejected"
            elif "pending" in prompt_lower:
                document_status = "Pending"

            # ------------------------------------------
            # Detect employee name
            # ------------------------------------------

            requested_employee = None

            employees = db.query(Employee).all()

            for candidate in employees:
                candidate_name = (
                    candidate.full_name.lower().strip()
                )

                if (
                    candidate_name
                    and candidate_name in prompt_lower
                ):
                    requested_employee = candidate
                    break

            # ------------------------------------------
            # Query documents
            # ------------------------------------------

            query = (
                db.query(EmployeeDocument, Employee)
                .join(
                    Employee,
                    EmployeeDocument.employee_id == Employee.id
                )
            )

            if requested_employee:
                query = query.filter(
                    EmployeeDocument.employee_id
                    == requested_employee.id
                )

            if document_status:
                query = query.filter(
                    func.lower(EmployeeDocument.status)
                    == document_status.lower()
                )

            records = (
                query
                .order_by(EmployeeDocument.id.desc())
                .all()
            )

            if not records:
                if requested_employee and document_status:
                    return (
                        f"No {document_status.lower()} documents found "
                        f"for {requested_employee.full_name}."
                    )

                if requested_employee:
                    return (
                        f"No documents found for "
                        f"{requested_employee.full_name}."
                    )

                if document_status:
                    return (
                        f"No {document_status.lower()} documents found."
                    )

                return "No documents found in the database."

            # ------------------------------------------
            # Format result
            # ------------------------------------------

            if requested_employee:
                lines = [
                    f"Documents for {requested_employee.full_name}:",
                    ""
                ]
            elif document_status:
                lines = [
                    f"{document_status} Documents:",
                    ""
                ]
            else:
                lines = [
                    "Employee Documents found in the database:",
                    ""
                ]

            for document, employee in records:

                lines.extend([
                    f"Document ID: {document.id}",
                    f"Employee ID: {employee.employee_id}",
                    f"Employee Name: {employee.full_name}",
                    f"Document Type: {document.document_type}",
                    f"Document Name: "
                    f"{document.document_name or 'Not provided'}",
                    f"Status: {document.status or 'Pending'}",
                    f"Remarks: "
                    f"{document.remarks or 'None'}",
                    f"Uploaded At: "
                    f"{document.uploaded_at or 'Not provided'}",
                    "-" * 45
                ])

            return "\n".join(lines)

        # ==========================================
        # PERFORMANCE DATABASE AI
        # ==========================================
        # Handles real Performance database queries.
        #
        # Examples:
        #   show all performance
        #   show Shyam performance
        #   show performance for Shyam
        #   show employees with rating above 3
        #   show employees with rating 4
        #   show highest rated employees
        #   show lowest rated employees

        if db is not None and (
            "performance" in prompt_lower
            or "rating" in prompt_lower
            or "rated" in prompt_lower
        ):

            # ------------------------------------------
            # Detect employee name
            # ------------------------------------------

            requested_employee = None

            employees = db.query(Employee).all()

            for candidate in employees:
                candidate_name = (
                    candidate.full_name.lower().strip()
                )

                if (
                    candidate_name
                    and candidate_name in prompt_lower
                ):
                    requested_employee = candidate
                    break

            # ------------------------------------------
            # Rating filters
            # ------------------------------------------

            rating_match = re.search(
                r"rating\s+(?:above|over|greater than)\s+([0-9]+)",
                prompt_lower
            )

            rating_equal_match = re.search(
                r"rating\s+(?:is\s+)?([0-9]+)",
                prompt_lower
            )

            rating_below_match = re.search(
                r"rating\s+(?:below|under|less than)\s+([0-9]+)",
                prompt_lower
            )

            # ------------------------------------------
            # Highest / lowest rating
            # ------------------------------------------

            if (
                "highest rating" in prompt_lower
                or "highest rated" in prompt_lower
                or "best rated" in prompt_lower
            ):

                record = (
                    db.query(Performance, Employee)
                    .join(
                        Employee,
                        Performance.employee_id == Employee.id
                    )
                    .order_by(
                        Performance.rating.desc(),
                        Performance.review_date.desc()
                    )
                    .first()
                )

                if not record:
                    return "No performance records found in the database."

                performance, employee = record

                return (
                    "Highest Rated Employee\n\n"
                    f"Name: {employee.full_name}\n"
                    f"Employee ID: {employee.employee_id}\n"
                    f"Designation: {employee.designation}\n"
                    f"Rating: {performance.rating}\n"
                    f"Review Date: {performance.review_date}\n"
                    f"Reviewer: {performance.reviewer}\n"
                    f"Promotion Status: "
                    f"{performance.promotion_status or 'Not Reviewed'}"
                )

            if (
                "lowest rating" in prompt_lower
                or "lowest rated" in prompt_lower
                or "worst rated" in prompt_lower
            ):

                record = (
                    db.query(Performance, Employee)
                    .join(
                        Employee,
                        Performance.employee_id == Employee.id
                    )
                    .order_by(
                        Performance.rating.asc(),
                        Performance.review_date.desc()
                    )
                    .first()
                )

                if not record:
                    return "No performance records found in the database."

                performance, employee = record

                return (
                    "Lowest Rated Employee\n\n"
                    f"Name: {employee.full_name}\n"
                    f"Employee ID: {employee.employee_id}\n"
                    f"Designation: {employee.designation}\n"
                    f"Rating: {performance.rating}\n"
                    f"Review Date: {performance.review_date}\n"
                    f"Reviewer: {performance.reviewer}\n"
                    f"Promotion Status: "
                    f"{performance.promotion_status or 'Not Reviewed'}"
                )

            # ------------------------------------------
            # Build performance query
            # ------------------------------------------

            query = (
                db.query(Performance, Employee)
                .join(
                    Employee,
                    Performance.employee_id == Employee.id
                )
            )

            if requested_employee:
                query = query.filter(
                    Performance.employee_id
                    == requested_employee.id
                )

            if rating_match:
                threshold = int(rating_match.group(1))

                query = query.filter(
                    Performance.rating > threshold
                )

            elif rating_below_match:
                threshold = int(rating_below_match.group(1))

                query = query.filter(
                    Performance.rating < threshold
                )

            elif rating_equal_match and "above" not in prompt_lower:
                rating = int(rating_equal_match.group(1))

                query = query.filter(
                    Performance.rating == rating
                )

            records = (
                query
                .order_by(
                    Performance.review_date.desc(),
                    Performance.id.desc()
                )
                .all()
            )

            if not records:

                if requested_employee:
                    return (
                        f"No performance records found for "
                        f"{requested_employee.full_name}."
                    )

                if rating_match:
                    return (
                        f"No employees found with performance "
                        f"rating above {rating_match.group(1)}."
                    )

                if rating_below_match:
                    return (
                        f"No employees found with performance "
                        f"rating below {rating_below_match.group(1)}."
                    )

                if rating_equal_match:
                    return (
                        f"No employees found with performance "
                        f"rating {rating_equal_match.group(1)}."
                    )

                return "No performance records found in the database."

            # ------------------------------------------
            # Format response
            # ------------------------------------------

            if requested_employee:
                lines = [
                    f"Performance for {requested_employee.full_name}:",
                    ""
                ]
            elif rating_match:
                lines = [
                    f"Employees With Rating Above "
                    f"{rating_match.group(1)}:",
                    ""
                ]
            elif rating_below_match:
                lines = [
                    f"Employees With Rating Below "
                    f"{rating_below_match.group(1)}:",
                    ""
                ]
            elif rating_equal_match:
                lines = [
                    f"Employees With Rating "
                    f"{rating_equal_match.group(1)}:",
                    ""
                ]
            else:
                lines = [
                    "Performance records found in the database:",
                    ""
                ]

            for performance, employee in records:

                lines.extend([
                    f"Name: {employee.full_name}",
                    f"Employee ID: {employee.employee_id}",
                    f"Designation: {employee.designation}",
                    f"Review Date: {performance.review_date}",
                    f"Rating: {performance.rating}",
                    f"Goals: "
                    f"{performance.goals or 'Not provided'}",
                    f"Strengths: "
                    f"{performance.strengths or 'Not provided'}",
                    f"Weaknesses: "
                    f"{performance.weaknesses or 'Not provided'}",
                    f"Feedback: "
                    f"{performance.feedback or 'Not provided'}",
                    f"Reviewer: {performance.reviewer}",
                    f"Promotion Status: "
                    f"{performance.promotion_status or 'Not Reviewed'}",
                    "-" * 45
                ])

            return "\n".join(lines)

        # ==========================================
        # EMPLOYEE DEPARTMENT AI
        # ==========================================
        # Handles questions such as:
        # "show shyam department"
        # "what department does shyam work in?"

        if db is not None and "department" in prompt_lower:

            employee_name = None

            # Pattern: "show <name> department"
            match = re.search(
                r"show\s+(.+?)\s+department",
                prompt_lower
            )

            if match:
                employee_name = match.group(1).strip()

            # Pattern: "what department does <name> work in?"
            if not employee_name:
                match = re.search(
                    r"what\s+department\s+does\s+(.+?)\s+work",
                    prompt_lower
                )

                if match:
                    employee_name = match.group(1).strip()

            # Pattern: "<name>'s department"
            if not employee_name:
                match = re.search(
                    r"(.+?)['’]s\s+department",
                    prompt_lower
                )

                if match:
                    employee_name = match.group(1).strip()

            if employee_name:

                employee = (
                    db.query(Employee)
                    .filter(
                        func.lower(Employee.full_name)
                        == employee_name.lower()
                    )
                    .first()
                )

                if not employee:
                    employee = (
                        db.query(Employee)
                        .filter(
                            Employee.full_name.ilike(
                                f"%{employee_name}%"
                            )
                        )
                        .first()
                    )

                if not employee:
                    return (
                        f"No employee found with the name "
                        f"'{employee_name}'."
                    )

                department_name = (
                    employee.department.department_name
                    if employee.department
                    else "Not assigned"
                )

                return (
                    "Employee Department\n\n"
                    f"Name: {employee.full_name}\n"
                    f"Employee ID: {employee.employee_id}\n"
                    f"Department: {department_name}\n"
                    f"Designation: {employee.designation}"
                )

        # ==========================================
        # ADMIN ATTENDANCE / LEAVE DATE AI
        # ==========================================
        # Supports:
        #   today's attendance
        #   yesterday's attendance
        #   attendance on 2026-08-18
        #   attendance 18/08/2026
        #   today's leaves
        #   yesterday's leaves
        #   leave on 2026-08-18
        #   leave 18/08/2026
        #
        # Admin users have employee_id=None.

        if db is not None and employee_id is None:

            query_date = None

            # ------------------------------------------
            # TODAY
            # ------------------------------------------
            if (
                "today" in prompt_lower
                or "todays" in prompt_lower
                or "today's" in prompt_lower
            ):
                query_date = date.today()

            # ------------------------------------------
            # YESTERDAY
            # ------------------------------------------
            elif "yesterday" in prompt_lower:
                query_date = date.today() - timedelta(days=1)

            # ------------------------------------------
            # SPECIFIC DATE: YYYY-MM-DD
            # Example: 2026-08-18
            # ------------------------------------------
            if query_date is None:
                match = re.search(
                    r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b",
                    prompt_lower
                )

                if match:
                    try:
                        query_date = date(
                            int(match.group(1)),
                            int(match.group(2)),
                            int(match.group(3))
                        )
                    except ValueError:
                        query_date = None

            # ------------------------------------------
            # SPECIFIC DATE: DD/MM/YYYY
            # Example: 18/08/2026
            # ------------------------------------------
            if query_date is None:
                match = re.search(
                    r"\b(\d{1,2})[-/](\d{1,2})[-/](20\d{2})\b",
                    prompt_lower
                )

                if match:
                    try:
                        query_date = date(
                            int(match.group(3)),
                            int(match.group(2)),
                            int(match.group(1))
                        )
                    except ValueError:
                        query_date = None

            # ------------------------------------------
            # ATTENDANCE DATE QUERY
            # ------------------------------------------
            if (
                query_date is not None
                and "attendance" in prompt_lower
            ):

                records = (
                    db.query(Attendance)
                    .filter(
                        Attendance.attendance_date == query_date
                    )
                    .order_by(
                        Attendance.id.desc()
                    )
                    .all()
                )

                if not records:
                    return (
                        f"No attendance records found for "
                        f"{query_date}."
                    )

                lines = [
                    f"Attendance for {query_date}:",
                    ""
                ]

                for record in records:

                    employee = (
                        db.query(Employee)
                        .filter(
                            Employee.id == record.employee_id
                        )
                        .first()
                    )

                    employee_name = (
                        employee.full_name
                        if employee
                        else "Unknown Employee"
                    )

                    lines.extend([
                        f"Employee ID: {record.employee_id}",
                        f"Name: {employee_name}",
                        f"Date: {record.attendance_date}",
                        f"Check In: {record.check_in or 'Not recorded'}",
                        f"Check Out: {record.check_out or 'Not recorded'}",
                        f"Status: {record.status or 'Not recorded'}",
                        f"Working Hours: {record.working_hours or 0}",
                        f"Late Minutes: {record.late_minutes or 0}",
                        f"Overtime Hours: {record.overtime_hours or 0}",
                        f"Attendance Type: {record.attendance_type or 'Not recorded'}",
                        f"Remarks: {record.remarks or 'None'}",
                        "-" * 45
                    ])

                return "\n".join(lines)

            # ------------------------------------------
            # LEAVE DATE QUERY
            # ------------------------------------------
            if (
                query_date is not None
                and (
                    "leave" in prompt_lower
                    or "leaves" in prompt_lower
                )
            ):

                records = (
                    db.query(LeaveRequest)
                    .filter(
                        LeaveRequest.start_date <= query_date,
                        LeaveRequest.end_date >= query_date
                    )
                    .order_by(
                        LeaveRequest.id.desc()
                    )
                    .all()
                )

                if not records:
                    return (
                        f"No leave records found for "
                        f"{query_date}."
                    )

                lines = [
                    f"Employee Leaves for {query_date}:",
                    ""
                ]

                for record in records:

                    employee = (
                        db.query(Employee)
                        .filter(
                            Employee.id == record.employee_id
                        )
                        .first()
                    )

                    employee_name = (
                        employee.full_name
                        if employee
                        else "Unknown Employee"
                    )

                    lines.extend([
                        f"Employee ID: {record.employee_id}",
                        f"Name: {employee_name}",
                        f"Leave Type: {record.leave_type}",
                        f"Start Date: {record.start_date}",
                        f"End Date: {record.end_date}",
                        f"Reason: {record.reason or 'Not provided'}",
                        f"Status: {record.status or 'Not recorded'}",
                        "-" * 45
                    ])

                return "\n".join(lines)

        # ==========================================
        # Attendance AI
        # ==========================================

        attendance_keywords = [
            "attendance",
            "present",
            "absent",
            "late",
            "attendance summary"
        ]

        if any(keyword in prompt_lower for keyword in attendance_keywords):

            if db is None or employee_id is None:
                return "Unable to retrieve attendance information."

            summary = attendance_ai.get_attendance_summary(
                db,
                employee_id
            )

            if not isinstance(summary, dict):
                return (
                    f"AttendanceAI returned an unexpected type: "
                    f"{type(summary).__name__}"
                )

            return llm.ask(
                f"""
You are an AI HR Assistant.

Employee Attendance Summary

Present : {summary.get('present', 0)}
Absent : {summary.get('absent', 0)}
Late : {summary.get('late', 0)}
Leave : {summary.get('leave', 0)}

Employee Question:
{prompt}

Instructions:
- Answer ONLY using the attendance information above.
- Mention exact values.
- Do not guess.
- Be professional.
"""
            )

        # ==========================================
        # Payroll AI
        # ==========================================

        payroll_keywords = [
            "salary",
            "payroll",
            "basic salary",
            "net salary",
            "bonus",
            "allowances",
            "deductions",
            "pay"
        ]

        if any(keyword in prompt_lower for keyword in payroll_keywords):

            if db is None or employee_id is None:
                return "Unable to retrieve payroll information."

            payroll = payroll_ai.get_payroll_summary(
                db,
                employee_id
            )

            if payroll is None:
                return "No payroll record found."

            return (
                "Employee Payroll Summary\n\n"
                f"Basic Salary: {payroll['basic_salary']}\n"
                f"Bonus: {payroll['bonus']}\n"
                f"Allowances: {payroll['allowances']}\n"
                f"Deductions: {payroll['deductions']}\n"
                f"Net Salary: {payroll['net_salary']}\n"
                f"Pay Date: {payroll['pay_date']}"
            )

        # Leave AI
        # ==========================================

        leave_keywords = [
            "leave",
            "leaves",
            "leave request",
            "leave history",
            "leave status",
            "approved leave",
            "pending leave",
            "rejected leave"
        ]

        if any(keyword in prompt_lower for keyword in leave_keywords):

            if db is None or employee_id is None:
                return "Unable to retrieve leave information."

            leave = leave_ai.get_leave_summary(
                db,
                employee_id
            )

            return llm.ask(
                f"""
You are an AI HR Assistant.

Employee Leave Summary

Approved Leaves : {leave['approved']}
Pending Leaves : {leave['pending']}
Rejected Leaves : {leave['rejected']}

Leave History:
{leave['history']}

Employee Question:
{prompt}

Instructions:
- Answer ONLY using the leave information above.
- Mention exact values.
- If asked about leave history, summarize it clearly.
- Do not guess.
- Be professional.
"""
            )

        # ==========================================
        # Employee Profile AI
        # ==========================================

        # ==========================================
        # ADMIN PROFILE AI
        # ==========================================

        if employee_id is None and any(
            keyword in prompt_lower
            for keyword in [
                "profile",
                "employee profile",
                "show profile",
                "show employee profile"
            ]
        ):

            # Try to identify an employee name from:
            # "show shyam profile"
            # "show harshita profile"
            # "show meghana profile"

            employees = (
                db.query(Employee)
                .order_by(Employee.id)
                .all()
            )

            target_employee = None

            for employee in employees:
                name = employee.full_name.lower()

                if name in prompt_lower:
                    target_employee = employee
                    break

            if target_employee is None:

                # "show my profile" cannot be resolved
                # when the logged-in Admin has no Employee record.
                if "my profile" in prompt_lower:
                    return (
                        "Admin profile is not linked to an employee record. "
                        "Please use 'show <employee name> profile'."
                    )

                return "Employee profile not found."

            profile = profile_ai.get_profile(
                db,
                target_employee.id
            )

            if profile is None:
                return "Employee profile not found."

            return (
                "Employee Profile\n\n"
                f"Employee ID: {profile['employee_id']}\n"
                f"Full Name: {profile['full_name']}\n"
                f"Email: {profile['email']}\n"
                f"Phone: {profile['phone'] or 'Not provided'}\n"
                f"Address: {profile['address'] or 'Not provided'}\n"
                f"Department: {profile['department'] or 'Not assigned'}\n"
                f"Designation: {profile['designation'] or 'Not provided'}\n"
                f"Salary: {profile['salary']}\n"
                f"Joining Date: {profile['joining_date'] or 'Not provided'}\n"
                f"Date of Birth: {profile['date_of_birth'] or 'Not provided'}\n"
                f"Nationality: {profile['nationality'] or 'Not provided'}\n"
                f"Emergency Contact: {profile['emergency_contact'] or 'Not provided'}"
            )

        # ==========================================
        # Employee Profile AI
        # ==========================================

        profile_keywords = [
            "profile",
            "my profile",
            "my name",
            "employee id",
            "my employee id",
            "my email",
            "my phone",
            "my address",
            "my department",
            "my designation",
            "my joining date",
            "my date of birth",
            "my nationality",
            "my emergency contact"
        ]

        if any(keyword in prompt_lower for keyword in profile_keywords):

            if db is None or employee_id is None:
                return "Unable to retrieve profile information."

            profile = profile_ai.get_profile(
                db,
                employee_id
            )

            if profile is None:
                return "Employee profile not found."

            # ==========================================
            # SECURITY CHECK
            # Employee can access ONLY their own data.
            # ==========================================

            other_employee_words = [
                "rahul",
                "harshita",
                "meghana",
                "other employee",
                "other employees",
                "all employees",
                "everyone"
            ]

            if any(word in prompt_lower for word in other_employee_words):
                return "Sorry, you are not authorized to access other employees' information."

            # ==========================================
            # FULL PROFILE
            # ==========================================

            if "profile" in prompt_lower:
                return (
                    "Employee Profile\n\n"
                    f"Employee ID: {profile['employee_id']}\n"
                    f"Full Name: {profile['full_name']}\n"
                    f"Email: {profile['email']}\n"
                    f"Phone: {profile['phone'] or 'Not provided'}\n"
                    f"Address: {profile['address'] or 'Not provided'}\n"
                    f"Department: {profile['department'] or 'Not assigned'}\n"
                    f"Designation: {profile['designation'] or 'Not provided'}\n"
                    f"Salary: {profile['salary']}\n"
                    f"Joining Date: {profile['joining_date'] or 'Not provided'}\n"
                    f"Date of Birth: {profile['date_of_birth'] or 'Not provided'}\n"
                    f"Nationality: {profile['nationality'] or 'Not provided'}\n"
                    f"Emergency Contact: {profile['emergency_contact'] or 'Not provided'}"
                )

            # ==========================================
            # INDIVIDUAL PROFILE INFORMATION
            # ==========================================

            if "employee id" in prompt_lower:
                return f"Your Employee ID is {profile['employee_id']}."

            if "my name" in prompt_lower:
                return f"Your name is {profile['full_name']}."

            if "my email" in prompt_lower:
                return f"Your email address is {profile['email']}."

            if "my phone" in prompt_lower:
                return f"Your phone number is {profile['phone'] or 'Not provided'}."

            if "my address" in prompt_lower:
                return f"Your address is {profile['address'] or 'Not provided'}."

            if "my department" in prompt_lower:
                return f"Your department is {profile['department'] or 'Not assigned'}."

            if "my designation" in prompt_lower:
                return f"Your designation is {profile['designation'] or 'Not provided'}."

            if "my joining date" in prompt_lower:
                return f"Your joining date is {profile['joining_date'] or 'Not provided'}."

            if "my date of birth" in prompt_lower:
                return f"Your date of birth is {profile['date_of_birth'] or 'Not provided'}."

            if "my nationality" in prompt_lower:
                return f"Your nationality is {profile['nationality'] or 'Not provided'}."

            if "my emergency contact" in prompt_lower:
                return f"Your emergency contact is {profile['emergency_contact'] or 'Not provided'}."

            return "I can provide information from your employee profile."

        # Performance AI
        # ==========================================

        performance_keywords = [
            "performance",
            "performance review",
            "review",
            "rating",
            "feedback",
            "strength",
            "strengths",
            "weakness",
            "weaknesses",
            "goal",
            "goals",
            "promotion",
            "promotion status",
            "reviewer"
        ]

        if any(keyword in prompt_lower for keyword in performance_keywords):

            if db is None or employee_id is None:
                return "Unable to retrieve performance information."

            performance = performance_ai.get_performance_summary(
                db,
                employee_id
            )

            if performance is None:
                return "No performance record found."

            return llm.ask(
                f"""
You are an AI HR Assistant.

Employee Performance Summary

Performance Rating : {performance['rating']}
Review Date : {performance['review_date']}
Goals : {performance['goals']}
Strengths : {performance['strengths']}
Weaknesses : {performance['weaknesses']}
Feedback : {performance['feedback']}
Reviewer : {performance['reviewer']}
Promotion Status : {performance['promotion_status']}

Employee Question:
{prompt}

Instructions:
- Answer ONLY using the performance information above.
- Mention exact values.
- Do not guess.
- Be professional.
"""
            )

        # ==========================================
        # Employee Database AI
        # ==========================================

        employee_list_keywords = [
            "show all employees",
            "list all employees",
            "all employees",
            "employee list",
            "employees list",
            "show employees",
            "list employees"
        ]

        if any(
            keyword in prompt_lower
            for keyword in employee_list_keywords
        ):

            if db is None:
                return "Unable to retrieve employee information."

            try:
                employees = (
                    db.query(Employee)
                    .order_by(Employee.id)
                    .all()
                )

                if not employees:
                    return "No employees found in the database."

                lines = [
                    "Employees found in the database:",
                    ""
                ]

                for employee in employees:

                    department_name = (
                        employee.department.department_name
                        if employee.department
                        else "Not assigned"
                    )

                    lines.append(
                        f"Employee ID: {employee.employee_id}\n"
                        f"Name: {employee.full_name}\n"
                        f"Email: {employee.email}\n"
                        f"Department: {department_name}\n"
                        f"Designation: {employee.designation}\n"
                        f"Salary: {employee.salary}\n"
                        f"Phone: {employee.phone or 'Not provided'}\n"
                        f"Address: {employee.address or 'Not provided'}\n"
                        f"Joining Date: {employee.joining_date or 'Not provided'}\n"
                        f"Date of Birth: {employee.date_of_birth or 'Not provided'}\n"
                        f"Nationality: {employee.nationality or 'Not provided'}\n"
                        f"Emergency Contact: "
                        f"{employee.emergency_contact or 'Not provided'}\n"
                        "----------------------------------------"
                    )

                return "\n".join(lines)

            except Exception as e:
                print("Employee database error:", e)
                return "Unable to retrieve employee information."

        # ==========================================
        # General HR AI
        # ==========================================

        try:
            return llm.ask(prompt)

        except Exception as e:
            print(e)

            return (
                "Sorry, the AI assistant is currently unavailable."
            )


ai_service = AIService()
