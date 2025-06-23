from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from typing import Any, cast, List
from app.db import models
from app.db.schemas import (
    EssayContent,
    MCQContent,
    Assessment,
)

# SQLite with async driver for concurrent access
DATABASE_URL = "sqlite+aiosqlite:///./assessment.db"
engine = create_async_engine(DATABASE_URL, echo=False)
# Session factory with autocommit disabled for explicit transaction control
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def create_practice_session(user_id: int, title: str | None):
    """Creates a new practice session with context manager for auto-cleanup"""
    async with SessionLocal() as session:
        new_session = models.PracticeSession(user_id=user_id, title=title)
        session.add(new_session)
        await session.commit()
        await session.refresh(new_session)
        return new_session.id


async def update_practice_session_title(session_id: int, title: str):
    # Use scalar_one_or_none for safe single-result query
    async with SessionLocal() as session:
        result = await session.execute(
            select(models.PracticeSession).where(
                models.PracticeSession.id == session_id
            )
        )
        practice_session = result.scalar_one_or_none()
        if not practice_session:
            return None

        practice_session.title = title  # type: ignore
        await session.commit()
        await session.refresh(practice_session)
        return session_id


async def save_uploaded_document(
    session_id: int,
    file_path: str,
    filename: str,
    content: str | None,  # Optional for non-text documents
    doc_metadata: dict | None,  # Stores file type, size, etc.
):
    async with SessionLocal() as session:
        doc = models.Document(
            session_id=session_id,
            filename=filename,
            path=file_path,
            content=content,
            doc_metadata=doc_metadata,
        )
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
        return doc.id


async def create_assessment(
    session_id: int, user_id: int, type_: str, content: EssayContent | MCQContent
):
    async with SessionLocal() as session:
        assessment = models.Assessment(
            session_id=session_id,
            user_id=user_id,
            type=type_,
            content=content.model_dump(),
        )
        session.add(assessment)
        await session.commit()
        await session.refresh(assessment)
        return assessment


async def update_assessment(
    session_id: int,
    answer: List[str],
    feedback: List[str],
    score: float | None,
) -> Assessment:
    async with SessionLocal() as session:
        result = await session.execute(
            select(models.Assessment).where(models.Assessment.session_id == session_id)
        )
        assessment = result.scalar_one_or_none()
        if not assessment:
            raise ValueError("Assessment not found for the given session ID")

        if answer is not None:
            assessment.answer = answer  # type: ignore
        if feedback is not None:
            assessment.feedback = feedback  # type: ignore
        if score is not None:
            assessment.score = cast(Any, score)

        await session.commit()
        await session.refresh(assessment)

        return assessment


async def get_document_by_session(session_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(models.Document).where(models.Document.session_id == session_id)
        )

        document = result.scalar_one_or_none()

        return document


async def get_assessment_by_session(session_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(models.Assessment).where(models.Assessment.session_id == session_id)
        )
        return result.scalar_one_or_none()


async def save_chat_message(user_id, session_id, message, sender):
    async with SessionLocal() as session:
        msg = models.ChatMessage(
            user_id=user_id, session_id=session_id, message=message, sender=sender
        )
        session.add(msg)
        await session.commit()
        await session.refresh(msg)
        return msg.id


async def load_chat_history(session_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(models.ChatMessage)
            .where(models.ChatMessage.session_id == session_id)
            .order_by(models.ChatMessage.created_at)
        )
        return result.scalars().all()


async def load_practice_sessions(user_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(models.PracticeSession)
            .where(models.PracticeSession.user_id == user_id)
            .order_by(models.PracticeSession.created_at.desc())
        )
        sessions = result.scalars().all()
        return sessions


async def get_session_by_id(session_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(models.PracticeSession).where(
                models.PracticeSession.id == session_id
            )
        )
        return result.scalar_one_or_none()


async def check_session_exists(session_id: int) -> bool:
    async with SessionLocal() as session:
        result = await session.execute(
            select(models.PracticeSession).where(
                models.PracticeSession.id == session_id
            )
        )
        return result.scalar_one_or_none() is not None
