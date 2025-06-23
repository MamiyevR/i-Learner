import React from "react";
import type { PracticeSession } from "../types";
import LoadingSpinner from "./LoadingSpinner";

interface SidebarProps {
    practices: PracticeSession[];
    onStartNew: () => void;
    onSelectPractice: (id: number) => void;
    selectedPracticeId?: number;
    isLoading?: boolean;
}

// Helper function to format date
// Formats date from "YYYY-MM-DDTHH:MM:SSZ" to "DD-MM-YY, HH:MM"
const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const dd = String(date.getDate()).padStart(2, '0');
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const yy = String(date.getFullYear()).slice(-2);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${dd}-${mm}-${yy}, ${hours}:${minutes}`;
};

const Sidebar: React.FC<SidebarProps> = ({ practices, onStartNew, onSelectPractice, selectedPracticeId, isLoading }) => {
    return (
        <aside className="Sidebar-root">
            <button className="Sidebar-new-btn" onClick={onStartNew} disabled={isLoading}>
                + New Practice
            </button>
            <div className="Sidebar-history-label">Practice History</div>
            <ul className="Sidebar-list">
                {isLoading ? (
                    <li className="Sidebar-loading">
                        <LoadingSpinner size="small" />
                    </li>
                ) : practices.length === 0 ? (
                    <li className="Sidebar-empty">No practices yet.</li>
                ) : (
                    practices.map(practice => (
                        <li
                            key={practice.id}
                            className={`Sidebar-item${selectedPracticeId === practice.id ? " selected" : ""}`}
                            onClick={() => onSelectPractice(practice.id)}
                        >
                            <div className="Sidebar-item-title">{practice.title}</div>
                            <div className="Sidebar-item-date">{formatDate(practice.created_at)}</div>
                        </li>
                    ))
                )}
            </ul>
        </aside>
    );
};

export default Sidebar;