from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import (
    RegisterRequest, LoginRequest, AuthSessionDTO,
    ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=AuthSessionDTO, status_code=status.HTTP_200_OK)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """
    UC-001 & UC-002: Register or Log In with OAuth Providers (Google, Facebook)
    Verifies token, attaches provider to linked_providers array for existing accounts,
    and auto-provisions User and personal Organization (max_vehicles=3) in a single transaction.
    """
    return AuthService.register_or_login(db, req)

@router.post("/login", response_model=AuthSessionDTO, status_code=status.HTTP_200_OK)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """
    UC-004: User Password Authentication & Session Initiation
    Authenticates registered email & password credentials, verifies active user status (is_active / deleted_at IS NULL),
    and returns AuthSessionDTO.
    """
    return AuthService.login(db, req)

@router.post("/forgot-password", response_model=ForgotPasswordResponse, status_code=status.HTTP_200_OK)
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    UC-006: Forgot Password Request
    Issues a password reset JWT token with 5-minute expiration for a valid registered user.
    """
    return AuthService.forgot_password(db, req)

@router.post("/reset-password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    UC-006: Password Reset Execution
    Verifies reset token, validates password policy, and updates user password hash.
    """
    return AuthService.reset_password(db, req)

