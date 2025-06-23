from fastapi import APIRouter, HTTPException
from app.db.queries import (
    load_practice_sessions,
    get_document_by_session,
    get_assessment_by_session,
    load_chat_history,
    create_practice_session,
    get_session_by_id,
)
from app.db import schemas

router = APIRouter()


@router.post("/new_session/{user_id}", response_model=schemas.PracticeSessionBase)
async def new_session(user_id: int):
    """Create a new practice session for a user.
    Args:
        user_id (int): The ID of the user for whom the session is being created.
    Returns:
        PracticeSessionBase: The newly created practice session with its ID.
    """
    try:
        session_id = await create_practice_session(
            user_id=user_id, title="New Practice Session"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create new session: {str(e)}"
        )
    return {"id": session_id}


@router.get("/sessions/{user_id}", response_model=schemas.PracticeSessions)
async def get_sessions(user_id: int):
    """Retrieve all practice sessions for a given user."""
    try:
        practice_sessions = await load_practice_sessions(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to load practice sessions: {str(e)}"
        )
    return {"sessions": practice_sessions}


@router.get("/session/{session_id}", response_model=schemas.FullPracticeSession)
async def get_session(session_id: int):
    """Retrieve a specific practice session by session ID, including document, assessment, and messages."""
    try:
        session_exists = await get_session_by_id(session_id)
        if not session_exists:
            raise HTTPException(status_code=404, detail="Session not found.")
        document = await get_document_by_session(session_id)
        assessment = await get_assessment_by_session(session_id)
        messages = await load_chat_history(session_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load session: {str(e)}")
    return {
        "id": session_id,
        "document": document,
        "assessment": assessment,
        "chat_messages": messages,
    }
