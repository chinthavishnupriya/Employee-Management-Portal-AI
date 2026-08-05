import re


INTENTS = {

    "profile": [

        "profile",
        "my profile",
        "my details",
        "my information",
        "who am i",
        "employee id",
        "designation",
        "department",
        "phone",
        "email"

    ],

    "attendance": [

        "attendance",
        "attendance history",
        "attendance summary",
        "working hours",
        "present",
        "absent",
        "late",
        "late today",
        "check in",
        "check out",
        "overtime"

    ],

    "leave": [

        "leave",
        "leave history",
        "leave summary",
        "leave status",
        "leave balance",
        "approved leave",
        "pending leave",
        "rejected leave",
        "casual leave",
        "sick leave",
        "annual leave",
        "vacation"

    ],

    "payroll": [

        "payroll",
        "salary",
        "basic salary",
        "net salary",
        "bonus",
        "allowances",
        "deductions",
        "payslip",
        "salary slip",
        "pay slip"

    ],

    "employees": [

        "employee",
        "employees",
        "employee list",
        "staff",
        "team",
        "department employees",
        "employee details"

    ],

    "performance": [

        "performance",
        "performance report",
        "rating",
        "evaluation",
        "appraisal"

    ],

    "documents": [

        "document",
        "documents",
        "resume",
        "certificate",
        "offer letter",
        "id card"

    ],

    "policy": [

        "policy",
        "leave policy",
        "attendance policy",
        "payroll policy",
        "company policy",
        "office timing",
        "working hours",
        "notice period",
        "probation",
        "dress code",
        "benefits",
        "insurance",
        "pf",
        "esi",
        "holiday",
        "wfh",
        "work from home"

    ]

}


def classify_intent(question: str):

    question = question.lower()

    question = re.sub(r"[^\w\s]", " ", question)

    question = " ".join(question.split())

    for intent, keywords in INTENTS.items():

        for keyword in keywords:

            if keyword in question:

                print(f"Detected Intent: {intent}")

                return intent

    print("Detected Intent: general")

    return "general"