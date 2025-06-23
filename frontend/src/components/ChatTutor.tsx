import React, { useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { ChatTutorProps } from "../types";
import LoadingSpinner from "./LoadingSpinner";

const ChatTutor: React.FC<ChatTutorProps> = ({ messages, chatInput, isSending, onInputChange, onSend, isLoading }) => {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    return (
        <div className="ChatTutor-page">
            <div className="ChatTutor-messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`ChatTutor-msg ChatTutor-msg--${msg.sender === "user" ? "user" : "bot"}`}>
                        {msg.sender === "user" ? (
                            <span>{msg.message}</span>
                        ) : (
                            <ReactMarkdown
                                remarkPlugins={[remarkGfm]}
                                components={{
                                    p: ({ node, ...props }) => <p className="markdown-content" {...props} />
                                }}
                            >
                                {msg.message}
                            </ReactMarkdown>
                        )}
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
            {isLoading && (
                <div className="ChatTutor-loading">
                    <LoadingSpinner size="small" />
                    <span>Loading chat history...</span>
                </div>
            )}
            <form className="ChatTutor-form" onSubmit={onSend}>
                <input
                    className="ChatTutor-input"
                    value={chatInput}
                    onChange={e => onInputChange(e.target.value)}
                    placeholder="Type your question about this assessment..."
                    disabled={isSending || isLoading}
                />
                <button className="ChatTutor-send" type="submit" disabled={isSending}>Send</button>
            </form>
        </div>
    );
};

export default ChatTutor;
