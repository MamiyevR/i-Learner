from typing import Optional
from fastapi import UploadFile
from app.ai.provider import AIProvider
import re
import PyPDF2
import os

provider = AIProvider()


def extract_text_from_pdf(file: UploadFile) -> str:
    # Reset file pointer to ensure complete read
    file.file.seek(0)
    reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in reader.pages:
        # Concatenate text from each page, handling empty pages gracefully
        text += page.extract_text() or ""
    return text


def extract_text_from_txt(file: UploadFile) -> str:
    # Reset file pointer and decode with error handling for malformed UTF-8
    file.file.seek(0)
    return file.file.read().decode("utf-8", errors="ignore")


def clean_text(text: str) -> str:
    # Normalize whitespace while preserving semantic breaks
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with single space
    text = text.strip()
    return text


def process_uploaded_document(file: UploadFile) -> Optional[str]:
    """
    Extract and clean text from an uploaded document (PDF or TXT).
    Args:
        file (UploadFile): The uploaded file object.
    Returns:
        Optional[str]: Cleaned text content if extraction is successful, None otherwise.
    """
    # Handle different file types with appropriate extractors
    if file.content_type == "application/pdf":
        try:
            text = extract_text_from_pdf(file)
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return None
    elif file.content_type == "text/plain":
        try:
            text = extract_text_from_txt(file)
        except Exception as e:
            print(f"TXT extraction error: {e}")
            return None
    else:
        print(f"Unsupported file type: {file.content_type}")
        return None
    return clean_text(text)


async def summarize_document(file: UploadFile) -> Optional[dict]:
    """
    Process the uploaded document and return a summary of its content.
    Args:
        file (UploadFile): The uploaded file object.
    Returns:
        Optional[dict]: Summary of the document content if successful, None otherwise.
    """
    text = process_uploaded_document(file)
    if not text:
        return None

    # Summarize the cleaned text using AI provider
    summary = provider.execute(
        "summarize",
        data={
            "content": text,
        },
    )

    return {**summary, "content": text}


async def save_document(file: UploadFile) -> tuple[str, str]:
    """
    Save the file to storage and return file path.
    Args:
        file (UploadFile): The uploaded file object.
    Returns:
        tuple[str, str]: Tuple containing the file path and filename.
    """
    upload_dir = "uploaded_docs"
    os.makedirs(upload_dir, exist_ok=True)
    filename = file.filename or "uploaded_file"
    file_path = os.path.join(upload_dir, filename)

    # Save the uploaded file to disk
    with open(file_path, "wb") as out_file:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            out_file.write(chunk)

    return (file_path, filename)
