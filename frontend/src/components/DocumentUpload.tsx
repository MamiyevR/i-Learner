import React, { useRef } from "react";
import type { DocumentUploadProps } from "../types";
import LoadingSpinner from "./LoadingSpinner";

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onFileUpload, isLoading }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileUpload(e.target.files[0]);
    }
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      className={`document-upload-dropzone ${isLoading ? 'loading' : ''}`}
      onClick={() => !isLoading && fileInputRef.current?.click()}
    >
      {isLoading ? (
        <div className="document-upload-loading">
          <LoadingSpinner size="medium" />
          <div>Uploading document...</div>
        </div>
      ) : (
        <>
          <input
            type="file"
            accept=".pdf,.txt,.doc,.docx"
            ref={fileInputRef}
            style={{ display: "none" }}
            onChange={handleFileChange}
            disabled={isLoading}
          />
          <div className="document-upload-title">
            Drag & drop your document here
          </div>
          <div className="document-upload-subtitle">
            or click to select a file (PDF, TXT, DOC)
          </div>
        </>
      )}
    </div>
  );
};

export default DocumentUpload;
