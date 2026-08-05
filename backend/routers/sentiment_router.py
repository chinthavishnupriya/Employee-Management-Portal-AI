from fastapi import APIRouter
from pydantic import BaseModel

from backend.ai.sentiment_ai import sentiment_ai


router = APIRouter(
    prefix="/sentiment",
    tags=["Sentiment Analysis"]
)


class Feedback(BaseModel):
    feedback: str


@router.post("/analyze")
def analyze(data: Feedback):

    result = sentiment_ai.analyze(data.feedback)

    return {
        "result": result
    }