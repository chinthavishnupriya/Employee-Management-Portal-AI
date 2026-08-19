from backend.services.ai_router_service import route_question


def ask_hr_ai(
    question: str,
    role: str,
    email: str
):

    question_lower = question.lower().strip()
    role = (role or "").strip().lower()

    # ==========================================
    # EMPLOYEE RESTRICTIONS
    # ==========================================

    if role == "employee":

        restricted_keywords = [

            "all employees",
            "employee list",
            "list employees",
            "show employees",
            "show all employee",
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
                    "other employees' information."
                )

    # ==========================================
    # HR RESTRICTIONS
    # ==========================================

    elif role == "hr":

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
    # ADMIN
    # ==========================================

    elif role == "admin":
        pass

    # ==========================================
    # INVALID ROLE
    # ==========================================

    else:

        return "Invalid user role."

    # ==========================================
    # SEND TO AI ROUTER
    # ==========================================

    return route_question(
        question=question,
        role=role.title(),
        email=email
    )
