import React from "react";
import type { MCQAssessmentProps, MCQQuestion } from "../types";
import LoadingSpinner from "./LoadingSpinner";

const MCQAssessment: React.FC<MCQAssessmentProps> = ({ mcqContent, onSubmit, feedback, userAnswer, onUserAnswerChange, score, isLoading }) => {
    const questions = mcqContent.questions;

    const handleSelect = (qIdx: number, oIdx: number) => {
        const updatedAnswers = [...userAnswer];
        updatedAnswers[qIdx] = questions[qIdx].distractors[oIdx];
        onUserAnswerChange(updatedAnswers);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(userAnswer);
    };

    // Check if feedback is provided to determine if the quiz has been submitted
    const submitted = feedback && feedback.length > 0;

    return (
        <form onSubmit={handleSubmit} className="MCQAssessment-container">
            {!submitted && (
                <div className="MCQAssessment-user">
                    <h3>Your Answers</h3>
                    {questions.map((q: MCQQuestion, i: number) => (
                        <div key={i} className="MCQAssessment-question">
                            <div className="MCQAssessment-question-title">{i + 1}. {q.question}</div>
                            {q.distractors.map((opt: string, j: number) => (
                                <label key={j} className="MCQAssessment-option">
                                    <input
                                        type="radio"
                                        name={`q${i}`}
                                        checked={userAnswer[i] === opt}
                                        onChange={() => handleSelect(i, j)}
                                    />
                                    {opt}
                                </label>
                            ))}
                        </div>
                    ))}
                    <button
                        type="submit"
                        className="MCQAssessment-btn"
                        disabled={isLoading || userAnswer.length !== questions.length || userAnswer.some(answer => answer === null || answer === undefined || answer === "")}
                    >
                        {isLoading ? (
                            <>
                                <LoadingSpinner size="small" />
                                <span style={{ marginLeft: '8px' }}>Submitting...</span>
                            </>
                        ) : (
                            "Submit Quiz"
                        )}
                    </button>
                </div>
            )}
            {submitted && (
                <div className="MCQAssessment-feedback">
                    <div className="MCQAssessment-grade">
                        <span>Score: <strong>{score}</strong></span>
                    </div>
                    {questions.map((q: MCQQuestion, i: number) => (
                        <div key={i} className="MCQAssessment-question">
                            <div className="MCQAssessment-feedback-title">{i + 1}. {q.question}</div>
                            <div className="MCQAssessment-feedback-options">
                                {q.distractors.map((opt: string, j: number) => {
                                    const isUserSelected = userAnswer[i] === opt;
                                    const isCorrect = opt === q.correct_answer;
                                    return (
                                        <div key={j} className="MCQAssessment-feedback-option">
                                            <span>{opt}</span>
                                            {isCorrect && <span className="MCQAssessment-correct-icon"> ✔️</span>}
                                            {isUserSelected && !isCorrect && <span className="MCQAssessment-incorrect-icon"> ❌</span>}
                                        </div>
                                    );
                                })}
                            </div>
                            {feedback[i] && (
                                <div className="MCQAssessment-explanation">
                                    <strong>Feedback:</strong> {feedback[i]}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </form>
    );
};

export default MCQAssessment;
