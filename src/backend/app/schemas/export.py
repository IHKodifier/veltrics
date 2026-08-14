from typing import Optional
from pydantic import BaseModel, EmailStr

class ExportEmailRequest(BaseModel):
    target_email: str

class ExportEmailResponse(BaseModel):
    status: str = "sent"
    message: str
    recipient: str
