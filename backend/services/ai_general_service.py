from backend.ai.llm_service import llm


GENERAL_RESTRICTED_KEYWORDS = [

    "all employees",
    "employee list",
    "attendance report",
    "payroll report",
    "leave report",
    "performance report",
    "analytics",
    "dashboard",
    "salary of",
    "employee salary",
    "department salary",
    "resume",
    "recruitment",
    "hire",
    "fire",
    "terminate",
    "delete employee",
    "update employee",
    "add employee",
    "system settings",
    "admin settings"

]


class general_ai:

    @staticmethod
    def ask(
        question: str,
        role: str
    ):

        question_lower = question.lower()

        # ==========================================
        # Employee Restrictions
        # ==========================================

        if role == "Employee":

            for keyword in GENERAL_RESTRICTED_KEYWORDS:

                if keyword in question_lower:

                    return (
                        "Sorry, you are not authorized "
                        "to access this information."
                    )

        # ==========================================
        # HR Restrictions
        # ==========================================

        if role == "HR":

            restricted = [

                "delete database",
                "drop database",
                "system settings",
                "admin settings"

            ]

            for keyword in restricted:

                if keyword in question_lower:

                    return (
                        "Sorry, only Administrators "
                        "can perform this operation."
                    )

        # ==========================================
        # AI Prompt
        # ==========================================

        prompt = f"""
You are an intelligent HR AI Assistant.

Current User Role

{role}

Rules

Employee
---------
- Answer only HR-related questions.
- Never reveal another employee's information.
- Never reveal payroll reports.
- Never reveal attendance reports.
- Never reveal company analytics.

HR
--
- Can answer HR operational questions.
- Can answer employee management questions.
- Cannot perform Administrator-only actions.

Admin
-----
- Can answer every HR question.
- Can access reports and analytics.

Question

{question}

Instructions

1. Answer professionally.

2. Keep the answer concise.

3. Never invent company information.

4. If the answer is unknown, reply:

"I don't have enough information to answer that question."

"""

        return llm.ask(prompt)