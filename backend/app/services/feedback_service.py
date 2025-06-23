from app.db.queries import get_assessment_by_session, get_document_by_session
from app.ai.provider import AIProvider
from app.db.schemas import FeedbackWithScore

provider = AIProvider()


def mcq_feedback(
    questions: list[str], user_answers: list[str], correct_answers: list[str]
) -> FeedbackWithScore:
    """Generate feedback and score for multiple-choice questions (MCQ).
    Args:
        questions (list[str]): List of question texts.
        user_answers (list[str]): List of user's answers.
        correct_answers (list[str]): List of correct answers.
    Returns:
        FeedbackWithScore: An object containing feedback and score.
    """

    # Validate input arrays have matching lengths
    if len(user_answers) != len(correct_answers):
        raise ValueError("User answers length must match correct answers length")
    if len(questions) != len(correct_answers):
        raise ValueError("Questions length must match correct answers length")

    # Calculate raw score based on exact matches
    score = sum(
        1
        for user_answer, correct_answer in zip(user_answers, correct_answers)
        if user_answer == correct_answer
    )

    # Generate detailed AI feedback for each answer
    ai_feedback = provider.execute(
        "grade_mcq",
        {
            "questions": questions,
            "user_answers": user_answers,
            "correct_answers": correct_answers,
        },
    )

    return FeedbackWithScore(feedback=ai_feedback.get("feedback", []), score=score)


def essay_feedback(essay_text, prompt, expected_answer, content) -> FeedbackWithScore:
    # Request AI-based analysis comparing student essay against expected answer
    ai_feedback = provider.execute(
        "grade_essay",
        {
            "essay": essay_text,
            "prompt": prompt,
            "expected_answer": expected_answer,
            "content": content,
        },
    )

    # Convert AI feedback to EssayFeedback type
    return FeedbackWithScore(
        feedback=[ai_feedback.get("feedback", "")],
        score=ai_feedback.get("score", 0.0),
    )


async def process_assessment_feedback(
    session_id: int, user_answer: list[str]
) -> FeedbackWithScore:
    # Retrieve assessment by id
    assessment = await get_assessment_by_session(session_id)
    document = await get_document_by_session(session_id)
    if not document:
        raise ValueError("Document not found for the given session ID")
    if not assessment:
        raise ValueError("Assessment not found")
    if str(assessment.type) == "mcq":
        return await process_mcq_feedback(assessment, user_answers=user_answer)
    elif str(assessment.type) == "essay":
        prompt = assessment.content.get("prompt", "")
        expected_answer = assessment.content.get("expected_answer", "")
        content = str(document.content) or ""
        return await process_essay_feedback(
            prompt, expected_answer, user_answer[0], content
        )
    else:
        raise ValueError("Unknown assessment type")


async def process_mcq_feedback(assessment, user_answers: list) -> FeedbackWithScore:
    questions = assessment.content.get("questions", [])
    question_texts = [q["question"] for q in questions]
    correct_answers = [q["correct_answer"] for q in questions]
    return mcq_feedback(question_texts, user_answers, correct_answers)


async def process_essay_feedback(
    prompt: str, expected_answer: str, essay_text: str, content: str
) -> FeedbackWithScore:
    return essay_feedback(essay_text, prompt, expected_answer, content)
