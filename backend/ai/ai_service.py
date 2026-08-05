from backend.ai.llm_service import llm
from backend.ai.attendance_ai import attendance_ai
from backend.ai.payroll_ai import payroll_ai
from backend.ai.leave_ai import leave_ai
from backend.ai.profile_ai import profile_ai
from backend.ai.performance_ai import performance_ai


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

            return llm.ask(
                f"""
You are an AI HR Assistant.

Employee Payroll Summary

Basic Salary : {payroll['basic_salary']}
Bonus : {payroll['bonus']}
Allowances : {payroll['allowances']}
Deductions : {payroll['deductions']}
Net Salary : {payroll['net_salary']}
Pay Date : {payroll['pay_date']}

Employee Question:
{prompt}

Instructions:
- Answer ONLY using the payroll information above.
- Mention exact salary values.
- Do not guess.
- Be professional.
"""
            )

        # ==========================================
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

        profile_keywords = [
            "profile",
            "my profile",
            "my name",
            "employee id",
            "email",
            "phone",
            "address",
            "department",
            "designation",
            "joining date",
            "date of birth",
            "nationality",
            "emergency contact"
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

            return llm.ask(
                f"""
You are an AI HR Assistant.

Employee Profile

Employee ID : {profile['employee_id']}
Full Name : {profile['full_name']}
Email : {profile['email']}
Phone : {profile['phone']}
Address : {profile['address']}
Department : {profile['department']}
Designation : {profile['designation']}
Salary : {profile['salary']}
Joining Date : {profile['joining_date']}
Date of Birth : {profile['date_of_birth']}
Nationality : {profile['nationality']}
Emergency Contact : {profile['emergency_contact']}

Employee Question:
{prompt}

Instructions:
- Answer ONLY using the employee profile above.
- Mention exact values.
- Do not guess.
- Be professional.
"""
            )

        # ==========================================
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