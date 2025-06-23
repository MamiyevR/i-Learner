from fastapi import APIRouter, UploadFile, File, HTTPException
from app.db.queries import save_uploaded_document
from app.services.document_service import process_uploaded_document, save_document
from app.db import schemas

router = APIRouter()


@router.post("/upload/{session_id}", response_model=schemas.DocumentBase)
async def upload_document(session_id: int, file: UploadFile = File(...)):
    # Validate file type
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF, and TXT files are allowed.",
        )

    try:
        # Process the uploaded document to extract and clean text
        content = process_uploaded_document(file)
        if not content or not content.strip():
            raise HTTPException(
                status_code=400, detail="Failed to extract text from the document."
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Document processing failed: {str(e)}"
        )

    doc_metadata = {
        "content_type": file.content_type,
        "size": getattr(file, "size", None),
    }

    try:
        # Save the file to storage and get the document metadata
        (file_path, filename) = await save_document(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    try:
        id = await save_uploaded_document(
            session_id, file_path, filename, content=content, doc_metadata=doc_metadata
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to save document: {str(e)}"
        )

    return {
        "id": id,
        "filename": filename,
        "path": file_path,
    }
