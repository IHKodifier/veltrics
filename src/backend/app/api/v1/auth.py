from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import GoogleRegisterRequest, AuthSessionDTO
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=AuthSessionDTO, status_code=status.HTTP_200_OK)
def register_with_google(req: GoogleRegisterRequest, db: Session = Depends(get_db)):
    """
    UC-001: Sign Up with Google One-Tap
    Verifies token, auto-provisions User and personal Organization (max_vehicles=3) in single transaction.
    """
    return AuthService.register_or_login_google(db, req)
