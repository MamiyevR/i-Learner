# Database models for the assessment system
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    JSON,
    Float,
    CheckConstraint,
)
import datetime

# SQLite database configuration
DATABASE_URL = "sqlite+aiosqlite:///./assessment.db"
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        Integer, ForeignKey("practice_sessions.id"), unique=True, nullable=False
    )
    filename = Column(String, index=True)
    path = Column(String)
    content = Column(Text)
    doc_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))


class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        Integer, ForeignKey("practice_sessions.id"), unique=True, nullable=False
    )
    user_id = Column(Integer, index=True)
    type = Column(String, nullable=False)  # 'essay' or 'mcq'
    content = Column(JSON)  # Stores questions/prompts
    answer = Column(JSON)  # Student's answers
    feedback = Column(JSON)  # AI-generated feedback
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )
    __table_args__ = (
        CheckConstraint("type IN ('mcq', 'essay')", name="check_assessment_type"),
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    session_id = Column(Integer, ForeignKey("practice_sessions.id"))
    message = Column(Text)
    sender = Column(String)  # 'user' or 'bot'
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    __table_args__ = (
        CheckConstraint("sender IN ('user', 'bot')", name="check_chatmessage_sender"),
    )


class PracticeSession(Base):
    __tablename__ = "practice_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
