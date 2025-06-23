import React from "react";
import type { EssayAssessmentProps } from "../types";
import LoadingSpinner from "./LoadingSpinner";

const EssayAssessment: React.FC<EssayAssessmentProps> = ({ essayContent, userAnswer, onUserAnswerChange, onSubmit, feedback, score, isLoading }) => {
    const wordCount = userAnswer.trim().split(/\s+/).filter(Boolean).length;
    const minWords = 300;
    const maxWords = 400;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit([userAnswer]);
    };

    const splitClass = feedback ? "EssayAssessment-split with-feedback" : "EssayAssessment-split no-feedback";

    return (
        <form onSubmit={handleSubmit} className="EssayAssessment-container">
            <div className={splitClass}>
                {/* Left: User's answer */}
                <div className="EssayAssessment-user">
                    <h3>Your Essay</h3>
                    <div className="EssayAssessment-prompt">
                        <strong>Prompt:</strong> {essayContent.prompt}
                    </div>
                    <textarea
                        value={userAnswer}
                        onChange={e => onUserAnswerChange(e.target.value)}
                        rows={12}
                        className="EssayAssessment-textarea"
                        placeholder="Write your essay here..."
                        disabled={!!feedback}
                    />
                    <div className="EssayAssessment-wordcount">
                        Word count: {wordCount} (required: {minWords}–{maxWords})
                    </div>
                    {!feedback && (
                        <button
                            type="submit"
                            className="EssayAssessment-btn"
                            disabled={wordCount < minWords || wordCount > maxWords || isLoading}
                        >
                            {isLoading ? (
                                <>
                                    <LoadingSpinner size="small" />
                                    <span style={{ marginLeft: '8px' }}>Submitting...</span>
                                </>
                            ) : (
                                "Submit Essay"
                            )}
                        </button>
                    )}
                </div>
                {/* Right: Feedback and evaluation */}
                {feedback && (
                    <div className={"EssayAssessment-feedback-panel active"}>
                        <h3>Feedback</h3>
                        <div className="EssayAssessment-feedback-content">
                            <div>{feedback}</div>
                            <div className="EssayAssessment-grade">Overall Grade: <strong>{score}</strong></div>
                        </div>
                        <h3>Expected Essay</h3>
                        <textarea
                            value={essayContent.expected_answer}
                            rows={12}
                            className="EssayAssessment-textarea"
                            placeholder="Write your essay here..."
                            disabled={true}
                        />
                    </div>
                )}
            </div>
        </form>
    );
};

export default EssayAssessment;
