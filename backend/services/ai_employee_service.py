from backend.ai.llm_service import llm

from backend.services.employee_service import (
    get_employee_details
)

from backend.services.attendance_service import (
    attendance_analytics
)

from backend.services.leave_service import (
    get_leave_requests
)

from backend.services.payroll_service import (
    get_payrolls
)


class employee_ai:

    @staticmethod
    def ask(
        question: str,
        role: str,
        intent: str,
        email: str
    ):

        # ==========================================
        # EMPLOYEE DETAILS
        # ==========================================

        if intent == "employees":

            employees = get_employee_details()

            context = ""

            for emp in employees:

                context += f"""

Employee ID : {emp["employee_id"]}

Employee Name : {emp["full_name"]}

Department : {emp["department"]}

Designation : {emp["designation"]}

Email : {emp["email"]}

Salary : {emp["salary"]}

"""

            prompt = f"""
You are an HR AI Assistant.

Current User Role

{role}

Employee Data

{context}

Question

{question}

Answer ONLY using the employee data.

Do not invent employee information.
"""

            return llm.ask(prompt)

        # ==========================================
        # ATTENDANCE ANALYTICS
        # ==========================================

        elif intent == "attendance":

            analytics = attendance_analytics()

            prompt = f"""
You are an HR AI Assistant.

Attendance Analytics

Present Today : {analytics["present_today"]}

Late Today : {analytics["late_today"]}

Absent Today : {analytics["absent_today"]}

Average Working Hours : {analytics["average_working_hours"]}

Total Overtime Hours : {analytics["total_overtime_hours"]}

Question

{question}

Answer ONLY using the attendance analytics.
"""

            return llm.ask(prompt)

        # ==========================================
        # LEAVE REPORT
        # ==========================================

        elif intent == "leave":

            leaves = get_leave_requests()

            context = ""

            for leave in leaves:

                context += f"""

Employee : {leave["employee_name"]}

Leave Type : {leave["leave_type"]}

Start Date : {leave["start_date"]}

End Date : {leave["end_date"]}

Status : {leave["status"]}

"""

            prompt = f"""
You are an HR AI Assistant.

Leave Records

{context}

Question

{question}

Answer ONLY using the leave records.
"""

            return llm.ask(prompt)

        # ==========================================
        # PAYROLL REPORT
        # ==========================================

        elif intent == "payroll":

            payrolls = get_payrolls()

            context = ""

            for payroll in payrolls:

                context += f"""

Employee : {payroll["employee"]}

Department : {payroll["department"]}

Basic Salary : {payroll["basic_salary"]}

Bonus : {payroll["bonus"]}

Allowances : {payroll["allowances"]}

Deductions : {payroll["deductions"]}

Net Salary : {payroll["net_salary"]}

Pay Date : {payroll["pay_date"]}

"""

            prompt = f"""
You are an HR AI Assistant.

Payroll Records

{context}

Question

{question}

Answer ONLY using the payroll records.
"""

            return llm.ask(prompt)

        # ==========================================
        # PERFORMANCE
        # ==========================================

        elif intent == "performance":

            prompt = f"""
You are an HR Performance Assistant.

Current User Role

{role}

Question

{question}

Answer professionally.

If no performance data exists,
say it is unavailable.
"""

            return llm.ask(prompt)

        # ==========================================
        # DOCUMENTS
        # ==========================================

        elif intent == "documents":

            prompt = f"""
You are an HR Document Assistant.

Current User Role

{role}

Question

{question}

Answer professionally.

If document information is unavailable,
say so.
"""

            return llm.ask(prompt)

        # ==========================================
        # GENERAL HR / ADMIN
        # ==========================================

        prompt = f"""
You are an HR AI Assistant.

Current User Role

{role}

Question

{question}

Answer professionally.

Never invent employee records.

If information is unavailable,
say:

"The requested information is unavailable."
"""

        return llm.ask(prompt)