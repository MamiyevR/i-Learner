from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ai.provider import AIProvider
from app.db.queries import (
    save_chat_message,
    get_document_by_session,
    get_assessment_by_session,
)
from app.db.schemas import Assessment

router = APIRouter()

provider = AIProvider()


class ChatRequest(BaseModel):
    user_id: int
    message: str
    document_content: str | None
    assessment: Assessment | None


class ChatResponse(BaseModel):
    response: str


@router.post("/chat/{session_id}", response_model=ChatResponse)
async def chat_api(session_id: int, request: ChatRequest):
    user_id = request.user_id
    message = request.message

    document = await get_document_by_session(session_id)
    assessment = await get_assessment_by_session(session_id)
    if document is None:
        raise HTTPException(
            status_code=404, detail="Document not found for this session."
        )
    if assessment is None:
        raise HTTPException(
            status_code=404, detail="Assessment not found for this session."
        )

    await save_chat_message(user_id, session_id, message, sender="user")

    try:
        response = provider.execute(
            "chat",
            data={
                "message": message,
                "assessment": assessment.content if assessment else None,
            },
        )
        if isinstance(response, dict) and "response" in response:
            response_text = response["response"]
        else:
            response_text = str(response)
        await save_chat_message(user_id, session_id, response_text, sender="bot")
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI model error: {str(e)}")
