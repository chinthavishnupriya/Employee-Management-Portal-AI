from backend.ai.llm_service import llm


class SentimentAI:

    def analyze(self, feedback: str):

        prompt = f"""
You are an HR Sentiment Analysis AI.

Analyze the following employee feedback.

Feedback:
{feedback}

Return ONLY in this format.

Sentiment: Positive / Neutral / Negative

Confidence: xx%

Reason:
One short sentence.
"""

        return llm.ask(prompt)


sentiment_ai = SentimentAI()