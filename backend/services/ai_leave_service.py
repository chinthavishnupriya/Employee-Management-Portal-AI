from backend.ai.llm_service import llm

from backend.services.leave_service import (
    get_my_leaves,
    get_leave_requests
)


LEAVE_KEYWORDS = [

    "leave",
    "my leave",
    "leave history",
    "leave summary",
    "leave status",
    "approved leave",
    "pending leave",
    "rejected leave",
    "leave balance",
    "casual leave",
    "sick leave",
    "annual leave",
    "vacation"

]


class leave_ai:

    @staticmethod
    def can_handle(question: str):

        question = question.lower()

        return any(

            keyword in question

            for keyword in LEAVE_KEYWORDS

        )

    @staticmethod
    def ask(
        question: str,
        email: str
    ):

        leaves = get_my_leaves(email)

        if len(leaves) == 0:

            return "No leave records found."

        context = ""

        for leave in leaves:

            context += f"""

Leave Type : {leave["leave_type"]}

Start Date : {leave["start_date"]}

End Date : {leave["end_date"]}

Reason : {leave["reason"]}

Status : {leave["status"]}

"""

        prompt = f"""
You are an HR AI Assistant.

The logged-in employee is asking ONLY about
their own leave information.

Never reveal another employee's leave.

Leave Records

{context}

Question

{question}

Instructions

1. Answer ONLY using the leave records.

2. Never invent leave details.

3. Never mention another employee.

4. If information is unavailable,
reply:

"The requested leave information is unavailable."
"""

        return llm.ask(prompt)