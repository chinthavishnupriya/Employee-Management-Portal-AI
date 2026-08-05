from backend.ai.llm_service import llm
from backend.services.employee_service import get_employee_profile


PROFILE_KEYWORDS = [

    "profile",
    "my profile",
    "show my profile",
    "who am i",
    "my details",
    "employee details",
    "my information",
    "my account",
    "designation",
    "department",
    "employee id",
    "phone",
    "email"

]


class profile_ai:

    @staticmethod
    def can_handle(question: str):

        question = question.lower()

        return any(

            keyword in question

            for keyword in PROFILE_KEYWORDS

        )

    @staticmethod
    def ask(
        question: str,
        email: str
    ):

        employee = get_employee_profile(email)

        if employee is None:

            return "Employee profile not found."

        prompt = f"""
You are an HR AI Assistant.

The user is asking ONLY about their own profile.

Never reveal information about another employee.

Employee Profile

Employee ID : {employee["employee_id"]}

Full Name : {employee["full_name"]}

Email : {employee["email"]}

Department : {employee["department"]}

Designation : {employee["designation"]}

Salary : {employee["salary"]}

Phone : {employee["phone"]}

Question

{question}

Instructions

1. Answer ONLY using the profile above.

2. Never invent information.

3. If the answer is unavailable,
reply:

"The requested information is not available."
"""

        return llm.ask(prompt)