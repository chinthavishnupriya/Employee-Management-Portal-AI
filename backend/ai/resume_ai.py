import os

from pypdf import PdfReader
from docx import Document

from backend.ai.llm_service import llm
from backend.ai.semantic_search import semantic_search


class ResumeAI:

    def extract_text(self, file_path: str):

        extension = os.path.splitext(file_path)[1].lower()

        text = ""

        if extension == ".pdf":

            reader = PdfReader(file_path)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        elif extension == ".docx":

            document = Document(file_path)

            for paragraph in document.paragraphs:
                text += paragraph.text + "\n"

        else:
            raise Exception("Unsupported file format.")

        return text.strip()

    def analyze_resume(self, file_path: str):

        resume_text = self.extract_text(file_path)

        # Add resume to semantic search index
        semantic_search.add_document(
            document_id=file_path,
            text=resume_text
        )

        prompt = f"""
You are an expert HR Recruiter.

Analyze the following resume.

Resume:

{resume_text}

Return the response in the following format:

Candidate Summary

Technical Skills

Soft Skills

Strengths

Weaknesses

Missing Skills

Recommended Job Role

ATS Score (0-100)

Interview Recommendation

Improvement Suggestions

Keep the response professional.
"""

        return llm.ask(prompt)


resume_ai = ResumeAI()