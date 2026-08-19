import os
import re

from pypdf import PdfReader
from docx import Document

from backend.ai.semantic_search import semantic_search


class ResumeAI:

    TECHNICAL_SKILLS = [
        "python", "java", "javascript", "typescript",
        "c", "c++", "c#", "sql", "html", "css",
        "react", "angular", "vue", "node.js", "node",
        "flask", "django", "fastapi",
        "postgresql", "mysql", "mongodb",
        "git", "github", "docker", "kubernetes",
        "aws", "azure", "gcp",
        "linux", "arduino", "esp32",
        "iot", "machine learning", "data analysis",
        "numpy", "pandas", "matlab"
    ]

    SOFT_SKILLS = [
        "communication", "leadership", "teamwork",
        "problem solving", "problem-solving",
        "time management", "adaptability",
        "critical thinking", "collaboration",
        "organization", "decision making",
        "decision-making", "creativity"
    ]

    COMMON_SKILLS = [
        "python", "sql", "git", "github",
        "html", "css", "javascript",
        "communication", "teamwork",
        "problem solving"
    ]

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

    def _find_skills(self, text, skills):

        text_lower = text.lower()

        found = []

        for skill in skills:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(skill)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text_lower):
                found.append(skill)

        return found

    def _calculate_ats_score(
        self,
        resume_text,
        technical_skills,
        soft_skills
    ):

        score = 0

        text_lower = resume_text.lower()

        # Technical skills: maximum 40 points

        technical_points = min(
            len(technical_skills) * 4,
            40
        )

        score += technical_points

        # Soft skills: maximum 20 points

        soft_points = min(
            len(soft_skills) * 4,
            20
        )

        score += soft_points

        # Resume structure: maximum 20 points

        sections = [
            "education",
            "experience",
            "skills",
            "project",
            "projects",
            "summary",
            "objective"
        ]

        section_count = sum(
            1
            for section in sections
            if section in text_lower
        )

        score += min(section_count * 4, 20)

        # Contact information: 5 points

        if re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            resume_text
        ):
            score += 5

        # Resume length/content: 10 points

        word_count = len(resume_text.split())

        if word_count >= 300:
            score += 10

        elif word_count >= 150:
            score += 5

        return min(score, 100)

    def _recommended_role(self, technical_skills):

        skills = set(technical_skills)

        if {"python", "flask"} <= skills:
            return "Python / Backend Developer"

        if {"react", "javascript"} <= skills:
            return "Frontend / React Developer"

        if (
            "python" in skills
            and (
                "numpy" in skills
                or "pandas" in skills
                or "machine learning" in skills
                or "data analysis" in skills
            )
        ):
            return "Python / Data Analyst"

        if (
            "sql" in skills
            and (
                "mysql" in skills
                or "postgresql" in skills
                or "mongodb" in skills
            )
        ):
            return "Database / Backend Developer"

        if (
            "arduino" in skills
            or "esp32" in skills
            or "iot" in skills
        ):
            return "Embedded / IoT Developer"

        if "python" in skills:
            return "Python Developer"

        if "javascript" in skills:
            return "JavaScript Developer"

        return "Entry-Level Software / IT Role"

    def _interview_recommendation(self, score):

        if score >= 80:
            return "Strongly Recommended"

        if score >= 65:
            return "Recommended"

        if score >= 50:
            return "Consider for Interview"

        return "Needs Improvement Before Interview"

    def _candidate_summary(
        self,
        technical_skills,
        soft_skills,
        recommended_role
    ):

        if not technical_skills:
            return (
                "The resume does not contain enough clearly "
                "identified technical skills for a detailed "
                "technical profile."
            )

        skill_text = ", ".join(technical_skills[:8])

        if len(technical_skills) > 8:
            skill_text += ", and other technical skills"

        return (
            f"The candidate demonstrates a technical profile "
            f"focused on {skill_text}. Based on the detected "
            f"skills, the most suitable role is "
            f"{recommended_role}."
        )

    def _strengths(
        self,
        technical_skills,
        soft_skills
    ):

        strengths = []

        if technical_skills:
            strengths.append(
                "Good technical skill coverage across: "
                + ", ".join(technical_skills[:6])
                + "."
            )

        if len(technical_skills) >= 8:
            strengths.append(
                "Broad technical skill set with exposure "
                "to multiple technologies."
            )

        if soft_skills:
            strengths.append(
                "The resume explicitly mentions soft skills such as: "
                + ", ".join(soft_skills)
                + "."
            )

        if not strengths:
            strengths.append(
                "No specific strengths could be confidently "
                "identified from the extracted resume content."
            )

        return strengths

    def _weaknesses(
        self,
        technical_skills,
        soft_skills,
        missing_skills
    ):

        weaknesses = []

        if missing_skills:
            weaknesses.append(
                "Some commonly expected skills are not detected: "
                + ", ".join(missing_skills)
                + "."
            )

        if not soft_skills:
            weaknesses.append(
                "Few or no explicit soft skills were detected "
                "in the resume."
            )

        if len(technical_skills) < 3:
            weaknesses.append(
                "The resume contains a limited number of "
                "detectable technical skills."
            )

        if not weaknesses:
            weaknesses.append(
                "No major weakness can be determined automatically "
                "from the extracted resume content."
            )

        return weaknesses

    def _improvement_suggestions(
        self,
        missing_skills,
        soft_skills,
        resume_text
    ):

        suggestions = []

        if missing_skills:
            suggestions.append(
                "Consider adding or demonstrating relevant skills: "
                + ", ".join(missing_skills)
                + "."
            )

        if not soft_skills:
            suggestions.append(
                "Add clearly demonstrated soft skills such as "
                "communication, teamwork, leadership, or "
                "problem solving where applicable."
            )

        if "project" not in resume_text.lower():
            suggestions.append(
                "Add clearly described projects with technologies "
                "used and measurable results where applicable."
            )

        if "experience" not in resume_text.lower():
            suggestions.append(
                "Include relevant experience, internships, or "
                "practical work where applicable."
            )

        if not suggestions:
            suggestions.append(
                "Continue improving the resume by quantifying "
                "achievements and keeping technical skills "
                "aligned with the target role."
            )

        return suggestions

    def analyze_resume(self, file_path: str):

        resume_text = self.extract_text(file_path)

        if not resume_text:
            return (
                "Unable to extract readable text from the resume."
            )

        # Add resume to semantic search index.

        semantic_search.add_document(
            document_id=file_path,
            text=resume_text
        )

        technical_skills = self._find_skills(
            resume_text,
            self.TECHNICAL_SKILLS
        )

        soft_skills = self._find_skills(
            resume_text,
            self.SOFT_SKILLS
        )

        detected_skill_names = {
            item.lower()
            for item in technical_skills + soft_skills
        }

        missing_skills = [
            skill
            for skill in self.COMMON_SKILLS
            if skill not in detected_skill_names
        ]

        ats_score = self._calculate_ats_score(
            resume_text,
            technical_skills,
            soft_skills
        )

        recommended_role = self._recommended_role(
            technical_skills
        )

        interview_recommendation = (
            self._interview_recommendation(ats_score)
        )

        candidate_summary = self._candidate_summary(
            technical_skills,
            soft_skills,
            recommended_role
        )

        strengths = self._strengths(
            technical_skills,
            soft_skills
        )

        weaknesses = self._weaknesses(
            technical_skills,
            soft_skills,
            missing_skills
        )

        improvement_suggestions = (
            self._improvement_suggestions(
                missing_skills,
                soft_skills,
                resume_text
            )
        )

        strength_text = "\n".join(
            f"- {item}"
            for item in strengths
        )

        weakness_text = "\n".join(
            f"- {item}"
            for item in weaknesses
        )

        improvement_text = "\n".join(
            f"- {item}"
            for item in improvement_suggestions
        )

        return (
            f"Candidate Resume Analysis\n\n"

            f"Candidate Summary\n"
            f"{candidate_summary}\n\n"

            f"Technical Skills\n"
            f"{', '.join(technical_skills) or 'None detected'}\n\n"

            f"Soft Skills\n"
            f"{', '.join(soft_skills) or 'None detected'}\n\n"

            f"Strengths\n"
            f"{strength_text}\n\n"

            f"Weaknesses\n"
            f"{weakness_text}\n\n"

            f"Missing Common Skills\n"
            f"{', '.join(missing_skills) or 'None detected'}\n\n"

            f"Recommended Job Role\n"
            f"{recommended_role}\n\n"

            f"ATS Score\n"
            f"{ats_score}/100\n\n"

            f"Interview Recommendation\n"
            f"{interview_recommendation}\n\n"

            f"Improvement Suggestions\n"
            f"{improvement_text}"
        )


resume_ai = ResumeAI()
