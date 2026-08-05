from backend.ai.llm_service import llm

from backend.services.payroll_service import (
    get_my_payroll,
    get_payrolls
)


PAYROLL_KEYWORDS = [

    "payroll",
    "salary",
    "my salary",
    "my payroll",
    "basic salary",
    "net salary",
    "bonus",
    "allowance",
    "allowances",
    "deduction",
    "deductions",
    "pay slip",
    "payslip",
    "salary slip"

]


class payroll_ai:

    @staticmethod
    def can_handle(question: str):

        question = question.lower()

        return any(

            keyword in question

            for keyword in PAYROLL_KEYWORDS

        )

    @staticmethod
    def ask(
        question: str,
        email: str
    ):

        payrolls = get_my_payroll(email)

        if not payrolls:

            return "No payroll records found."

        context = ""

        for payroll in payrolls:

            context += f"""

Pay Date : {payroll["pay_date"]}

Basic Salary : {payroll["basic_salary"]}

Bonus : {payroll["bonus"]}

Allowances : {payroll["allowances"]}

Deductions : {payroll["deductions"]}

Net Salary : {payroll["net_salary"]}

"""

        prompt = f"""
You are an HR AI Assistant.

The logged-in employee is asking ONLY
about their own payroll.

Never reveal another employee's payroll.

Payroll Records

{context}

Question

{question}

Instructions

1. Answer ONLY using the payroll records.

2. Never invent salary information.

3. Never mention another employee.

4. If the information is unavailable,
reply:

"The requested payroll information is unavailable."
"""

        answer = llm.ask(prompt)

        if answer is None:

            return "Unable to generate payroll response."

        return answer

    @staticmethod
    def ask_admin(
        question: str
    ):

        payrolls = get_payrolls()

        if not payrolls:

            return "No payroll records found."

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

        answer = llm.ask(prompt)

        if answer is None:

            return "Unable to generate payroll response."

        return answer