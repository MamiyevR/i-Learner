from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import datetime

AssessmentType = Literal["essay", "mcq"]


# Essay assessment types
class EssayContent(BaseModel):
    prompt: str = Field(description="Essay prompt generated from the content")
    expected_answer: str = Field(
        description="Expected essay answer based on the prompt and content"
    )


class Answer(BaseModel):
    answer: List[str]


class Feedback(BaseModel):
    feedback: List[str]


class FeedbackWithScore(Feedback):
    score: float


# Essay grading models
class EssayGradingResponse(BaseModel):
    score: float = Field(
        description="Essay score from 0-100",
        ge=0,  # greater than or equal to 0
        le=100,  # less than or equal to 100
    )
    feedback: str = Field(description="Feedback for the essay")


# MCQ grading models
class MCQGradingResponse(BaseModel):
    feedback: List[str] = Field(
        description="List of feedback for each multiple choice question"
    )


# Summary models
class SummaryResponse(BaseModel):
    summary: str = Field(description="Concise summary of the content")
    keyword: str = Field(
        description="One-two word keyword representing the main idea of the content"
    )


# MCQ assessment types
class MCQQuestion(BaseModel):
    question: str = Field(description="The question text")
    distractors: List[str] = Field(
        description="List of distractor options for the question"
    )
    correct_answer: str = Field(description="The correct answer to the question")


class MCQContent(BaseModel):
    questions: List[MCQQuestion] = Field(
        description="List of generated multiple choice questions with answers and distractors"
    )


class PracticeSessionBase(BaseModel):
    id: int


class PracticeSession(PracticeSessionBase):
    user_id: int
    title: str
    created_at: datetime.datetime


class PracticeSessions(BaseModel):
    sessions: List[PracticeSession]


class Assessment(BaseModel):
    id: int
    session_id: int
    user_id: int
    type: AssessmentType
    content: EssayContent | MCQContent
    answer: Optional[List[str]]
    feedback: Optional[List[str]]
    score: Optional[float]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]


class DocumentBase(BaseModel):
    id: int
    filename: str
    path: str


class Document(DocumentBase):
    session_id: int
    content: str
    doc_metadata: dict
    created_at: datetime.datetime


class ChatMessage(BaseModel):
    id: int
    user_id: int
    session_id: int
    sender: Literal["user", "bot"]
    message: str
    created_at: datetime.datetime


class FullPracticeSession(PracticeSessionBase):
    document: Optional[Document] = None
    assessment: Optional[Assessment] = None
    chat_messages: List[ChatMessage]
