import pdfplumber
from docx import Document
import re


class ResumeParser:

    def extract_text(self, file_path):

        if file_path.endswith(".pdf"):

            text = ""

            with pdfplumber.open(file_path) as pdf:

                for page in pdf.pages:
                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

            return text

        elif file_path.endswith(".docx"):

            doc = Document(file_path)

            return "\n".join(
                paragraph.text
                for paragraph in doc.paragraphs
            )

        return ""

    def parse(self, file_path):

        text = self.extract_text(file_path)

        email = ""

        phone = ""

        email_match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        if email_match:
            email = email_match.group()

        phone_match = re.search(
            r"\+?\d[\d\s-]{8,15}",
            text
        )

        if phone_match:
            phone = phone_match.group()

        skills = []

        skill_list = [
            "Python",
            "Java",
            "C",
            "C++",
            "React",
            "FastAPI",
            "HTML",
            "CSS",
            "JavaScript",
            "SQL",
            "PostgreSQL",
            "Machine Learning",
            "AI",
            "Docker",
            "AWS"
        ]

        for skill in skill_list:

            if skill.lower() in text.lower():
                skills.append(skill)

        return {
            "text": text,
            "email": email,
            "phone": phone,
            "skills": skills
        }


resume_parser = ResumeParser()