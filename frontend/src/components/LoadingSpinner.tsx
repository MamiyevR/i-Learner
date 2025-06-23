import React from 'react';
import './Loading.css';

interface LoadingSpinnerProps {
    size?: 'small' | 'medium' | 'large';
    overlay?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 'medium', overlay = false }) => {
    const spinnerClass = `loading-spinner loading-spinner-${size}`;

    if (overlay) {
        return (
            <div className="loading-overlay">
                <div className={spinnerClass}>
                    <div className="spinner"></div>
                </div>
            </div>
        );
    }

    return (
        <div className={spinnerClass}>
            <div className="spinner"></div>
        </div>
    );
};

export default LoadingSpinner;
