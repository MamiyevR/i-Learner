import React from "react";
import type { AssessmentTypeSelectorProps } from "../types";
import LoadingSpinner from "./LoadingSpinner";

const AssessmentTypeSelector: React.FC<AssessmentTypeSelectorProps> = ({ onSelect, isLoading }) => {
  return (
    <div className="AssessmentTypeSelector-container">
      <h2 className="AssessmentTypeSelector-title">Select Assessment Type</h2>
      {isLoading ? (
        <div className="AssessmentTypeSelector-loading">
          <LoadingSpinner size="medium" />
          <div>Generating assessment...</div>
        </div>
      ) : (
        <div className="AssessmentTypeSelector-btn-group">
          <button
            className="AssessmentTypeSelector-btn"
            onClick={() => onSelect("essay")}
            data-testid="select-essay"
            type="button"
            disabled={isLoading}
          >
            Essay
          </button>
          <button
            className="AssessmentTypeSelector-btn"
            onClick={() => onSelect("mcq")}
            data-testid="select-mcq"
            type="button"
            disabled={isLoading}
          >
            MCQ
          </button>
        </div>
      )}
    </div>
  );
};

export default AssessmentTypeSelector;
