export type AssessmentType = 'essay' | 'mcq';
export type Role = 'user' | 'bot';


export interface EssayContent {
    prompt: string;
    expected_answer?: string;
}


export interface MCQQuestion {
    question: string;
    correct_answer: string;
    distractors: string[];
}

export interface MCQContent {
    questions: MCQQuestion[];
}

export interface Assessment {
    id: number;
    session_id: number;
    user_id: number;
    type: AssessmentType;
    content: EssayContent | MCQContent;
    answer?: string[];
    feedback?: string[];
    score?: number;
    created_at: string;
    updated_at?: string;
}

export interface ChatMessage {
    id: number;
    userId: number;
    sessionId: number;
    message: string
    sender: Role;
    createdAt: string;
}

export interface ChatResponse {
    response: string;
}

export interface Document {
    id: number;
    session_id: number;
    filename: string;
    path: string;
    content: string;
    doc_metadata: {
        content_type: string;
        size: number;
    };
    created_at: string;
}

export interface PracticeSession {
    id: number;
    user_id: number;
    title: string;
    created_at: string;
}

export interface PracticeSessions {
    sessions: PracticeSession[];
}

export interface SelectedSession {
    id: number;
    document: Document | null;
    assessment: Assessment | null;
    chat_messages: ChatMessage[];
}

// Component Props Interfaces
export interface DocumentUploadProps {
    onFileUpload: (file: File) => void;
    isLoading?: boolean;
}

export interface AssessmentTypeSelectorProps {
    onSelect: (type: AssessmentType) => void;
    isLoading?: boolean;
}

export interface EssayAssessmentProps {
    essayContent: EssayContent;
    userAnswer: string;
    onUserAnswerChange: (answer: string) => void;
    onSubmit: (answer: string[]) => Promise<void>;
    feedback?: string;
    score: number;
    isLoading?: boolean;
}

export interface MCQAssessmentProps {
    mcqContent: MCQContent;
    onSubmit: (answer: string[]) => Promise<void>;
    feedback: string[];
    userAnswer: string[];
    onUserAnswerChange: (answers: string[]) => void;
    score: number;
    isLoading?: boolean;
}

export interface ChatTutorProps {
    messages: ChatMessage[];
    chatInput: string;
    isSending: boolean;
    onInputChange: (value: string) => void;
    onSend: (e: React.FormEvent) => Promise<void>;
    isLoading?: boolean;
}

export interface LoadingSpinnerProps {
    size?: 'small' | 'medium' | 'large';
    overlay?: boolean;
}