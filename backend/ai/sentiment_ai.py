import re


class SentimentAI:

    POSITIVE_WORDS = {
        "good",
        "great",
        "excellent",
        "positive",
        "outstanding",
        "strong",
        "successful",
        "success",
        "best",
        "better",
        "improved",
        "improvement",
        "helpful",
        "professional",
        "productive",
        "efficient",
        "reliable",
        "creative",
        "organized",
        "organization",
        "teamwork",
        "collaboration",
        "leadership",
        "achievement",
        "achieved",
        "commendable",
        "satisfied",
        "happy",
        "effective",
        "skilled",
        "excellent",
        "exceptional"
    }

    NEGATIVE_WORDS = {
        "bad",
        "poor",
        "negative",
        "weak",
        "weakness",
        "weaknesses",
        "problem",
        "problems",
        "issue",
        "issues",
        "difficult",
        "difficulty",
        "failed",
        "failure",
        "fail",
        "late",
        "delay",
        "delayed",
        "complaint",
        "complaints",
        "unsatisfied",
        "unhappy",
        "unprofessional",
        "inconsistent",
        "inefficient",
        "mistake",
        "mistakes",
        "error",
        "errors",
        "conflict",
        "conflicts",
        "overcommit",
        "overcommitting",
        "underestimate",
        "poorly"
    }

    def _clean(self, text):
        return re.sub(r"\s+", " ", text.strip())

    def _score(self, text):
        words = re.findall(r"[a-zA-Z]+", text.lower())

        positive = []
        negative = []

        for word in words:
            if word in self.POSITIVE_WORDS:
                positive.append(word)

            if word in self.NEGATIVE_WORDS:
                negative.append(word)

        return positive, negative

    def analyze(self, feedback: str):

        feedback = self._clean(feedback)

        if not feedback:
            return "Please enter employee feedback."

        positive_words, negative_words = self._score(feedback)

        positive_score = len(positive_words)
        negative_score = len(negative_words)

        # ------------------------------------------
        # Overall sentiment
        # ------------------------------------------

        if positive_score > 0 and negative_score > 0:
            sentiment = "Mixed"

        elif positive_score > negative_score:
            sentiment = "Positive"

        elif negative_score > positive_score:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

        # ------------------------------------------
        # Confidence
        # ------------------------------------------

        total_signals = positive_score + negative_score

        if total_signals >= 4:
            confidence = 95

        elif total_signals == 3:
            confidence = 90

        elif total_signals == 2:
            confidence = 85

        elif total_signals == 1:
            confidence = 75

        else:
            confidence = 50

        # ------------------------------------------
        # Explanation
        # ------------------------------------------

        if sentiment == "Mixed":
            reason = (
                "The feedback contains both positive and negative "
                "statements."
            )

        elif sentiment == "Positive":
            reason = (
                "The feedback contains predominantly positive "
                "language."
            )

        elif sentiment == "Negative":
            reason = (
                "The feedback contains predominantly negative "
                "language."
            )

        else:
            reason = (
                "The feedback does not contain enough clearly "
                "positive or negative language."
            )

        # ------------------------------------------
        # Result
        # ------------------------------------------

        lines = [
            "Employee Sentiment Analysis",
            "",
            f"Overall Sentiment: {sentiment}",
            f"Confidence: {confidence}%",
            "",
            "Feedback:",
            feedback,
            ""
        ]

        if positive_words:
            lines.extend([
                "Positive Indicators:",
                "- " + ", ".join(sorted(set(positive_words))),
                ""
            ])
        else:
            lines.extend([
                "Positive Indicators:",
                "- None detected",
                ""
            ])

        if negative_words:
            lines.extend([
                "Negative Indicators:",
                "- " + ", ".join(sorted(set(negative_words))),
                ""
            ])
        else:
            lines.extend([
                "Negative Indicators:",
                "- None detected",
                ""
            ])

        lines.extend([
            "Analysis:",
            reason
        ])

        return "\n".join(lines)


sentiment_ai = SentimentAI()
