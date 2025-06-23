import type { Document, Assessment, AssessmentType, PracticeSessions, SelectedSession, ChatResponse } from '../types';
const API_BASE_URL = import.meta.env.API_BASE_URL || 'http://localhost:8000';


export const api = {
  async uploadDocument(file: File, sessionId: number): Promise<Document> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_BASE_URL}/upload/${sessionId}`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Failed to upload document: ${response.statusText}`);
    }

    return response.json();
  },

  async generateTask(sessionId: number, assessmentType: AssessmentType): Promise<Assessment> {
    const response = await fetch(`${API_BASE_URL}/generate/${sessionId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        user_id: 1 , // Replace with actual user ID
        assessment_type:  assessmentType,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate task: ${response.statusText}`);
    }

    return response.json();
  },

  async getFeedback(sessionId: number, userAnswer: Array<string>): Promise<Assessment> {
    const response = await fetch(`${API_BASE_URL}/grade/${sessionId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_answer: userAnswer,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to get feedback: ${response.statusText}`);
    }

    return response.json();
  },

  async createSession(): Promise<number> {
    const response = await fetch(`${API_BASE_URL}/new_session/1`, { // Replace with actual user ID
        method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Failed to create session: ${response.statusText}`);
    }

    const data = await response.json();

    return data.id;
  },

  async getSessions(): Promise<PracticeSessions> {
    const response = await fetch(`${API_BASE_URL}/sessions/1`);  // Replace with actual user ID

    if (!response.ok) {
      throw new Error(`Failed to get sessions: ${response.statusText}`);
    }

    return response.json();
  },

  async getSession(sessionId: number): Promise<SelectedSession> {
    const response = await fetch(`${API_BASE_URL}/session/${sessionId}`);

    if (!response.ok) {
      throw new Error(`Failed to get session: ${response.statusText}`);
    }

    return response.json();
  },

  async chatWithBot(sessionId: number, userId: number, message: string, documentContent: string, assessment: Assessment | null): Promise<ChatResponse> {
    // Ensure assessment data matches backend expectations
    const requestBody = {
      user_id: userId,
      message: message,
      document_content: documentContent,
      assessment: assessment ? {
        ...assessment,
        // Ensure dates are in ISO format
        created_at: new Date(assessment.created_at).toISOString(),
        updated_at: assessment.updated_at ? new Date(assessment.updated_at).toISOString() : undefined
      } : null
    };

    const response = await fetch(`${API_BASE_URL}/chat/${sessionId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });
  
    if (!response.ok) {
      throw new Error(`Failed to get assistant response: ${response.statusText}`);
    }
  
    return response.json();
  }
}
