from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.feedback_service import process_assessment_feedback
from app.db.queries import update_assessment
from app.db.schemas import Assessment

router = APIRouter()


class GradeRequest(BaseModel):
    user_answer: List[str]


@router.post("/grade/{session_id}", response_model=Assessment)
async def grade_essay(session_id: int, req: GradeRequest):
    """Process feedback for an assessment based on user answers.
    Args:
        session_id (int): The ID of the session for which feedback is being processed.
        req (GradeRequest): The request containing user answers.
    Returns:
        Assessment: The updated assessment object with feedback and score.
    """
    if not req.user_answer or not isinstance(req.user_answer, list):
        raise HTTPException(
            status_code=400, detail="user_answer must be a non-empty list."
        )

    try:
        result = await process_assessment_feedback(
            session_id, user_answer=req.user_answer
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process feedback: {str(e)}"
        )

    if not result:
        raise HTTPException(
            status_code=500, detail="Failed to process feedback. Please try again."
        )

    try:
        # Update the assessment with the feedback, score, and user answer
        assessment = await update_assessment(
            session_id=session_id,
            answer=req.user_answer,
            feedback=result.feedback,
            score=result.score,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update assessment: {str(e)}"
        )

    if not assessment:
        raise HTTPException(status_code=500, detail="Failed to update assessment.")

    return assessment
