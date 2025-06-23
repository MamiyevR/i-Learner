from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.generate_service import generate_question
from app.db.queries import create_assessment
from app.db import schemas

router = APIRouter()


class GenerateRequest(BaseModel):
    user_id: int
    assessment_type: schemas.AssessmentType


@router.post("/generate/{session_id}", response_model=schemas.Assessment)
async def generate(session_id: int, req: GenerateRequest):
    """Generate an essay prompt or MCQ questions based on the session ID and assessment type."""
    try:
        # Generate the question based on the session ID and assessment type
        generated_question = await generate_question(session_id, req.assessment_type)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate question: {str(e)}"
        )

    if not generated_question:
        raise HTTPException(
            status_code=500, detail="Failed to generate question. Please try again."
        )

    try:
        # Update the assessment in the database with the generated question
        assessment = await create_assessment(
            session_id=session_id,
            user_id=req.user_id,
            type_=req.assessment_type,
            content=generated_question,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to save assessment: {str(e)}"
        )

    return assessment
