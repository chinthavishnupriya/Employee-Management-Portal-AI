from backend.services.ai_router_service import route_question


def ask_hr_ai(
    question: str,
    role: str,
    email: str
):

    question_lower = question.lower()

    # ==========================================
    # Employee Restrictions
    # ==========================================

    if role == "Employee":

        restricted_keywords = [

            "all employees",
            "employee list",
            "salary of",
            "attendance report",
            "payroll report",
            "leave report",
            "performance report",
            "analytics",
            "dashboard",
            "resume",
            "recruitment",
            "hire",
            "fire",
            "terminate",
            "delete employee",
            "update employee",
            "add employee"

        ]

        for keyword in restricted_keywords:

            if keyword in question_lower:

                return (
                    "Sorry, you are not authorized to access "
                    "this information."
                )

    # ==========================================
    # HR Restrictions
    # ==========================================

    elif role == "HR":

        restricted_keywords = [

            "delete database",
            "drop database",
            "system settings",
            "admin settings"

        ]

        for keyword in restricted_keywords:

            if keyword in question_lower:

                return (
                    "Sorry, only Administrators can "
                    "perform this action."
                )

    # ==========================================
    # Send to AI Router
    # ==========================================

    return route_question(

        question=question,
        role=role,
        email=email

    )