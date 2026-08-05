from backend.ai.intent_classifier import classify_intent

from backend.services.ai_profile_service import profile_ai
from backend.services.ai_attendance_service import attendance_ai
from backend.services.ai_leave_service import leave_ai
from backend.services.ai_payroll_service import payroll_ai
from backend.services.ai_employee_service import employee_ai
from backend.services.ai_policy_service import policy_ai
from backend.services.ai_general_service import general_ai


def route_question(
    question: str,
    role: str,
    email: str
):

    print("=" * 60)
    print("ROLE:", role)
    print("EMAIL:", email)
    print("QUESTION:", question)

    intent = classify_intent(question)

    print("INTENT:", intent)

    # ====================================
    # EMPLOYEE
    # ====================================

    if role == "Employee":

        if profile_ai.can_handle(question):
            return profile_ai.ask(question, email)

        elif attendance_ai.can_handle(question):
            return attendance_ai.ask(question, email)

        elif leave_ai.can_handle(question):
            return leave_ai.ask(question, email)

        elif payroll_ai.can_handle(question):
            return payroll_ai.ask(question, email)

        elif policy_ai.can_handle(question):
            return policy_ai.ask(question)

        else:
            return general_ai.ask(
                question=question,
                role=role
            )

    # ====================================
    # HR
    # ====================================

    elif role == "HR":

        return employee_ai.ask(

            question=question,
            role=role,
            intent=intent,
            email=email

        )

    # ====================================
    # ADMIN
    # ====================================

    elif role == "Admin":

        return employee_ai.ask(

            question=question,
            role=role,
            intent=intent,
            email=email

        )

    return "Invalid role."