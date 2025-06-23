import { useState, useEffect, useCallback } from "react";
import './App.css'
import './components/Loading.css'
import DocumentUpload from "./components/DocumentUpload";
import AssessmentTypeSelector from "./components/AssessmentTypeSelector";
import EssayAssessment from "./components/EssayAssessment";
import MCQAssessment from "./components/MCQAssessment";
import ChatTutor from "./components/ChatTutor";
import Sidebar from "./components/Sidebar";
import type { ChatMessage, PracticeSession, SelectedSession, EssayContent, MCQContent, Assessment, Document, AssessmentType } from "./types";
import { api } from "./services/api";


const App: React.FC = () => {
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [document, setDocument] = useState<Document | null>(null);
  const [essayContent, setEssayContent] = useState<EssayContent | null>(null);
  const [mcqContent, setMcqContent] = useState<MCQContent | null>(null);
  const [feedback, setFeedback] = useState<string[]>([]);
  const [userAnswer, setUserAnswer] = useState<string[]>([]);
  const [score, setScore] = useState<number>(0);
  const [showChat, setShowChat] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [practices, setPractices] = useState<PracticeSession[]>([]);
  const [selectedPracticeId, setSelectedPracticeId] = useState<number | undefined>(undefined);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [chatInput, setChatInput] = useState("");
  const [isChatSending, setIsChatSending] = useState(false);
  const userId = 1; // Placeholder for actual user ID

  const fetchSessions = useCallback(async () => {
    try {
      setIsLoading(true);
      const fetchedSessions = await api.getSessions();
      setPractices(fetchedSessions.sessions);
    } catch (error) {
      console.error("Error fetching sessions:", error);
      setError("Failed to load practice history.")
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  const createNewSession = async () => {
    try {
      const newSessionId = await api.createSession();
      setSessionId(newSessionId);
      setAssessment(null);
      setDocument(null);
      setEssayContent(null);
      setMcqContent(null);
      setFeedback([]);
      setUserAnswer([]);
      setScore(0);
      setShowChat(false);
      setChatMessages([]);
      setSelectedPracticeId(undefined);
      fetchSessions(); // Refresh sessions after creating a new one
      setIsLoading(true);
      setError(null);
    } catch (error) {
      console.error("Error creating session:", error);
      setError("Failed to create new practice.")
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (file: File) => {
    if (sessionId) {
      try {
        setIsLoading(true);
        setError(null);
        fetchSessions(); // Refresh sessions to ensure the latest data is displayed
        const response = await api.uploadDocument(file, sessionId);
        setDocument(response);
      } catch (error) {
        console.error("Error uploading document:", error);
        setError("Failed to upload document.");
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleEssayUserAnswerChange = (answer: string) => {
    setUserAnswer([answer]);
  };

  const handleMCQUserAnswerChange = (answers: string[]) => {
    setUserAnswer(answers);
  };

  const handleChatInputChange = (value: string) => {
    setChatInput(value);
  };

  const handleChatSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim() || isChatSending || !sessionId) return;
    setChatMessages((msgs) => [
      ...msgs,
      { id: 0, userId: userId, sessionId: sessionId, message: chatInput, sender: "user", createdAt: new Date().toISOString() }
    ]);
    setIsChatSending(true);
    try {
      const response = await api.chatWithBot(sessionId, userId, chatInput, document ? document.content : "", assessment);
      if (response.response) {
        setChatMessages((msgs) => [
          ...msgs,
          { id: 0, userId: userId, sessionId: sessionId, sender: "bot", message: response.response, createdAt: new Date().toISOString() }
        ]);
      } else if ((response as any).error) {
        setChatMessages((msgs) => [
          ...msgs,
          { id: 0, userId: userId, sessionId: sessionId, message: (response as any).error, sender: "bot", createdAt: new Date().toISOString() }
        ]);
      }
    } catch (err) {
      setChatMessages((msgs) => [
        ...msgs,
        { id: 0, userId: userId, sessionId: sessionId, message: "Failed to get response from tutor.", sender: "bot", createdAt: new Date().toISOString() }
      ]);
    } finally {
      setIsChatSending(false);
      setChatInput("");
    }
  };

  const handleSubmit = async (answer: string[]) => {
    if (sessionId) {
      try {
        setIsLoading(true);
        setError(null); // Clear previous errors
        const feedbackResponse = await api.getFeedback(sessionId, answer);
        setFeedback(feedbackResponse.feedback ? feedbackResponse.feedback : []);
        if (feedbackResponse.type === "essay") {
          setEssayContent(feedbackResponse.content as EssayContent);
        } else if (feedbackResponse.type === "mcq") {
          setMcqContent(feedbackResponse.content as MCQContent)
        }
        setUserAnswer(feedbackResponse.answer ? feedbackResponse.answer : [])
        setScore(feedbackResponse.score ? feedbackResponse.score : 0);
      } catch (error) {
        console.error("Error submitting assessment:", error);
        setError("Error submitting assessment. Please try again")
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleStartNew = () => {
    createNewSession(); // Call the async function to create a new session
  };

  const handleSelectPractice = async (id: number) => {
    setSelectedPracticeId(id);

    try {
      setIsLoading(true);
      setError(null);
      const sessionData: SelectedSession = await api.getSession(id);
      setSessionId(sessionData.id);
      setAssessment(sessionData.assessment);
      setDocument(sessionData.document);
      setFeedback(sessionData.assessment?.feedback ? sessionData.assessment.feedback : []);
      setUserAnswer(sessionData.assessment?.answer ? sessionData.assessment.answer : []);
      setScore(sessionData.assessment?.score ? sessionData.assessment.score : 0);

      if (sessionData.assessment?.type === "essay") {
        setEssayContent(sessionData.assessment.content as EssayContent);
      } else if (sessionData.assessment?.type === "mcq") {
        setMcqContent(sessionData.assessment.content as MCQContent);
      }
      setChatMessages(sessionData.chat_messages.map(msg => ({
        id: msg.id,
        userId: msg.userId,
        sessionId: msg.sessionId,
        message: msg.message,
        sender: msg.sender,
        createdAt: msg.createdAt,
      })));
      setShowChat(sessionData.chat_messages.length > 0);
    } catch (error) {
      console.error("Error fetching session:", error);
      setError("Error fetching session")
    } finally {
      setIsLoading(false);
    }
  };

  const handleAssessmentSelect = async (type: AssessmentType) => {
    if (sessionId) {
      try {
        setIsLoading(true);
        setError(null);
        const assessment = await api.generateTask(sessionId, type);
        setAssessment(assessment);
        setScore(0);
        setFeedback([]);
        setUserAnswer([]);

        // Populate assessment details based on the response
        if (assessment.type === "essay") {
          setEssayContent(assessment.content as EssayContent);
        } else if (assessment.type === "mcq") {
          setMcqContent(assessment.content as MCQContent);
        }
      } catch (error) {
        console.error("Error generating task:", error);
        setError("Error generating task. Please try again")
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="App">
      {/* {isLoading && <LoadingSpinner overlay />} */}
      <Sidebar
        practices={practices}
        onStartNew={handleStartNew}
        onSelectPractice={handleSelectPractice}
        selectedPracticeId={selectedPracticeId}
        isLoading={isLoading}
      />
      <div style={{ marginLeft: 270, minHeight: "100vh" }}>
        <h1 style={{ textAlign: "center", marginTop: 32 }}>i-Learner: Upload Educational Document</h1>
        {error && (
          <div className="error-message" style={{
            color: 'red',
            textAlign: 'center',
            marginTop: '16px',
            padding: '8px',
            backgroundColor: '#fff1f1',
            borderRadius: '4px',
            maxWidth: '600px',
            margin: '16px auto'
          }}>
            {error}
          </div>
        )}
        {!document && sessionId && (
          <DocumentUpload onFileUpload={handleFileUpload} isLoading={isLoading} />
        )}
        {document && !assessment && (
          <>
            <div style={{ textAlign: "center", marginTop: 24 }}>
              <strong>Uploaded:</strong> {document.filename}
            </div>
            <AssessmentTypeSelector onSelect={handleAssessmentSelect} isLoading={isLoading} />
          </>
        )}
        {document && assessment?.type === "essay" && essayContent && (
          <>
            <EssayAssessment
              essayContent={essayContent}
              userAnswer={userAnswer[0] ? userAnswer[0] : ""}
              onUserAnswerChange={handleEssayUserAnswerChange}
              onSubmit={handleSubmit}
              feedback={feedback[0]}
              score={score}
              isLoading={isLoading}
            />
            {(!showChat && assessment?.feedback) && (
              <div style={{ display: "flex", justifyContent: "center", marginTop: 24, marginBottom: 24 }}>
                <button className="MCQAssessment-chat-btn" onClick={() => setShowChat(true)} type="button">
                  Chat with AI Tutor
                </button>
              </div>
            )}
            {showChat && sessionId && userId && (
              <ChatTutor
                messages={chatMessages}
                chatInput={chatInput}
                isSending={isChatSending}
                onInputChange={handleChatInputChange}
                onSend={handleChatSend}
                isLoading={isLoading}
              />
            )}
          </>
        )}
        {document && assessment?.type === "mcq" && mcqContent && (
          <>
            <MCQAssessment
              mcqContent={mcqContent}
              onSubmit={handleSubmit}
              feedback={feedback}
              userAnswer={userAnswer}
              onUserAnswerChange={handleMCQUserAnswerChange}
              score={score}
              isLoading={isLoading}
            />
            {(!showChat && assessment?.feedback) && (
              <div style={{ display: "flex", justifyContent: "center", marginTop: 24, marginBottom: 24 }}>
                <button className="MCQAssessment-chat-btn" onClick={() => setShowChat(true)} type="button">
                  Chat with AI Tutor
                </button>
              </div>
            )}
            {showChat && sessionId && userId && (
              <ChatTutor
                messages={chatMessages}
                chatInput={chatInput}
                isSending={isChatSending}
                onInputChange={handleChatInputChange}
                onSend={handleChatSend}
                isLoading={isLoading}
              />
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default App
