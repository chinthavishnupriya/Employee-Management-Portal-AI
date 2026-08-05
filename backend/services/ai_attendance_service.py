from backend.ai.llm_service import llm

from backend.services.attendance_service import (
    my_attendance,
    my_summary,
    attendance_analytics
)


ATTENDANCE_KEYWORDS = [

    "attendance",
    "my attendance",
    "attendance history",
    "attendance summary",
    "today attendance",
    "present",
    "absent",
    "late",
    "late today",
    "working hours",
    "check in",
    "check out",
    "overtime"

]


class attendance_ai:

    @staticmethod
    def can_handle(question: str):

        question = question.lower()

        return any(

            keyword in question

            for keyword in ATTENDANCE_KEYWORDS

        )

    @staticmethod
    def ask(
        question: str,
        email: str
    ):

        records = my_attendance(email)

        summary = my_summary(email)

        if isinstance(records, dict):

            return records.get(
                "message",
                "No attendance records found."
            )

        context = ""

        for record in records:

            context += f"""

Date : {record["date"]}

Status : {record["status"]}

Check In : {record["check_in"]}

Check Out : {record["check_out"]}

Working Hours : {record["working_hours"]}

Late Minutes : {record["late_minutes"]}

Overtime Hours : {record["overtime_hours"]}

Attendance Type : {record["attendance_type"]}

Remarks : {record["remarks"]}

"""

        prompt = f"""
You are an HR AI Assistant.

The employee is asking ONLY about
their own attendance.

Attendance Summary

Total Days : {summary["total_days"]}

Present : {summary["present"]}

Late : {summary["late"]}

Total Working Hours : {summary["total_working_hours"]}

Total Overtime : {summary["total_overtime"]}

Attendance Records

{context}

Question

{question}

Instructions

1. Answer ONLY using the attendance data above.

2. Never mention another employee.

3. Never invent attendance.

4. If information is unavailable,
reply:

"The requested attendance information is unavailable."
"""

        return llm.ask(prompt)