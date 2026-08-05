from backend.ai.llm_service import llm


POLICY_KEYWORDS = [

    "policy",
    "leave policy",
    "attendance policy",
    "payroll policy",
    "company policy",
    "office timing",
    "office timings",
    "working hours",
    "working days",
    "notice period",
    "probation",
    "probation period",
    "dress code",
    "benefits",
    "insurance",
    "pf",
    "esi",
    "holiday",
    "vacation",
    "wfh",
    "work from home"

]


class policy_ai:

    @staticmethod
    def can_handle(question: str):

        question = question.lower()

        return any(

            keyword in question

            for keyword in POLICY_KEYWORDS

        )

    @staticmethod
    def ask(question: str):

        company_policy = """

Company HR Policies

-----------------------------------

Working Days
-------------
Monday to Friday

Office Timing
-------------
09:00 AM to 06:00 PM

Attendance
----------
Employees must check in and check out
every working day.

Late Policy
-----------
Employees arriving more than
15 minutes late are marked Late.

Leave Policy
------------
Leave requests must be approved
before the leave starts.

Payroll
--------
Salary is processed every month.

Benefits
---------
• Health Insurance

• Paid Leave

• Performance Bonus

• Provident Fund (PF)

• Employee State Insurance (ESI)

Notice Period
-------------
30 Days

Probation
----------
6 Months

Dress Code
----------
Business Casual

Work From Home
--------------
Allowed only with Manager approval.

"""

        prompt = f"""
You are an HR AI Assistant.

Answer ONLY using the company
policy below.

Company Policy

{company_policy}

Question

{question}

Instructions

1. Never invent company policies.

2. If information is unavailable,
reply:

"The requested policy information is unavailable."

3. Keep answers professional.
"""

        return llm.ask(prompt)