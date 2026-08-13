import os
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException, status

router = APIRouter(prefix="/uploads", tags=["Uploads"])

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../uploads/receipts"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/receipt", status_code=status.HTTP_201_CREATED)
async def upload_receipt(file: UploadFile = File(...)):
    """
    UC-063: Upload receipt image file.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename cannot be empty"
        )

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp", ".pdf"]:
        ext = ".jpg"

    unique_filename = f"rec_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    file_url = f"/uploads/receipts/{unique_filename}"

    return {
        "file_url": file_url,
        "filename": unique_filename,
        "original_filename": file.filename,
        "size_bytes": len(contents)
    }
