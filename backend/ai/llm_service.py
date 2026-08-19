import os
import json
import urllib.request
import urllib.error


class LLMService:

    def __init__(self):

        self.model = "tinyllama:latest"

        self.host = os.getenv(
            "OLLAMA_HOST",
            "http://172.17.0.1:11434"
        ).rstrip("/")

        self.system_prompt = """
You are Corporate AI Assistant for an Employee Management Portal.

Your primary responsibility is to assist employees, managers, HR staff,
payroll teams, and administrators in their daily work.

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

        prompt = prompt.strip()

        if not prompt:
            return "Please enter your question."

        full_prompt = (
            self.system_prompt
            + "\n\nUser Question:\n"
            + prompt
        )

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False
        }

        try:

            data = json.dumps(payload).encode("utf-8")

            request = urllib.request.Request(
                f"{self.host}/api/generate",
                data=data,
                headers={
                    "Content-Type": "application/json"
                },
                method="POST"
            )

            with urllib.request.urlopen(
                request,
                timeout=120
            ) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

            answer = result.get("response")

            if answer:
                return answer.strip()

            return "The AI returned an empty response."

        except urllib.error.URLError as e:

            print(
                f"Ollama connection error: {e}",
                flush=True
            )

            return (
                "Sorry, the AI assistant is currently unavailable."
            )

        except Exception as e:

            print(
                f"Ollama AI error: {type(e).__name__}: {e}",
                flush=True
            )

            return (
                "Sorry, the AI assistant is currently unavailable."
            )


llm = LLMService()
