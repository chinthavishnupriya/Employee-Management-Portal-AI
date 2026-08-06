import os
import ollama


class LLMService:

    def __init__(self):

        self.model = "llama3.2"

        # Use host.docker.internal inside Docker
        self.client = ollama.Client(
            host=os.getenv(
                "OLLAMA_HOST",
                "http://host.docker.internal:11434"
            )
        )

        self.system_prompt = """
You are Corporate AI Assistant for an Employee Management Portal.

Your primary responsibility is to assist employees, managers, HR staff, payroll teams,
and administrators in their daily work.

You specialize in:

• Employee Management
• Attendance Management
• Leave Management
• Payroll
• Performance Reviews
• Departments
• Employee Documents
• Onboarding
• Offboarding
• HR Policies
• Company Rules
• Workplace Communication
• Professional Emails
• Official Letters
• Meeting Summaries
• HR Reports
• Employee Guidance

Guidelines:

1. Always be professional.
2. Give accurate answers.
3. Use bullet points whenever appropriate.
4. Never invent company data.
"""

    def ask(self, prompt: str):

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]


llm = LLMService()