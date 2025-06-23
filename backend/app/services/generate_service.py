# Service for generating assessment content using AI
from app.db.queries import get_document_by_session, update_practice_session_title
from app.ai.provider import AIProvider
from app.db.schemas import EssayContent, MCQContent, MCQQuestion
import random

provider = AIProvider()


async def generate_essay_prompt(content: str) -> EssayContent:
    """
    Generate an essay prompt and expected answer based document content.
    """
    # Request AI to generate essay question
    generated_question = provider.execute(
        "essay",
        {
            "content": content,
        },
    )
    if not generated_question:
        raise ValueError("Failed to generate essay prompt")

    # Format the response into structured essay content
    essay_content = EssayContent(
        prompt=generated_question.get("prompt", ""),
        expected_answer=generated_question.get("expected_answer", ""),
    )
    return essay_content


async def generate_mcq_questions(content: str) -> MCQContent:
    """
    Generate MCQ questions, answers, and distractors based on Session_id.
    """
    # Generate multiple choice questions using AI
    generated_question = provider.execute(
        "mcq",
        {
            "content": content,
        },
    )
    if not generated_question:
        raise ValueError("Failed to generate MCQ questions")

    questions_data = generated_question.get("questions", [])
    if not questions_data:
        raise ValueError("No questions were generated")

    # Create MCQContent object
    mcq_content = MCQContent(
        questions=[
            MCQQuestion(
                question=q.get("question", ""),
                correct_answer=q.get("correct_answer", ""),
                distractors=(lambda d: random.sample(d, len(d)))(
                    q.get("distractors", [])
                ),
            )
            for q in questions_data
        ]
    )

    return mcq_content


async def generate_question(
    session_id: int, assessment_type: str
) -> EssayContent | MCQContent:
    """
    Generate content based on the session ID and type.
    """
    # retrieve document content for the session
    document = await get_document_by_session(session_id)
    if not document:
        raise ValueError("Document not found for the given session ID")
    elif document.content is None or document.content.strip() == "":
        raise ValueError("Document content is empty")

    # update session title
    await update_practice_session_title(
        session_id=session_id, title=f"{document.filename} - {assessment_type}"
    )

    if assessment_type == "essay":
        return await generate_essay_prompt(str(document.content))
    elif assessment_type == "mcq":
        return await generate_mcq_questions(str(document.content))
    else:
        raise ValueError("Unknown generation type. Use 'essay' or 'mcq'.")
