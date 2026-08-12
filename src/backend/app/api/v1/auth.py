from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import (
    RegisterRequest, LoginRequest, AuthSessionDTO,
    ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse,
    RefreshTokenRequest, RefreshTokenResponse, LogoutRequest, LogoutResponse
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=AuthSessionDTO, status_code=status.HTTP_200_OK)
def register(req: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    """
    UC-001 & UC-002: Register or Log In with OAuth Providers (Google, Facebook)
    Verifies token, attaches provider to linked_providers array for existing accounts,
    and auto-provisions User and personal Organization (max_vehicles=3) in a single transaction.
    """
    return AuthService.register_or_login(db, req, request=request)

@router.post("/login", response_model=AuthSessionDTO, status_code=status.HTTP_200_OK)
def login(req: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """
    UC-004: User Password Authentication & Session Initiation
    Authenticates registered email & password credentials, verifies active user status (is_active / deleted_at IS NULL),
    and returns AuthSessionDTO.
    """
    return AuthService.login(db, req, request=request)

@router.post("/forgot-password", response_model=ForgotPasswordResponse, status_code=status.HTTP_200_OK)
def forgot_password(req: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """
    UC-006: Forgot Password Request
    Issues a password reset JWT token with 5-minute expiration for a valid registered user.
    """
    return AuthService.forgot_password(db, req, request=request)

@router.post("/reset-password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
def reset_password(req: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """
    UC-006: Password Reset Execution
    Verifies reset token, validates password policy, and updates user password hash.
    """
    return AuthService.reset_password(db, req, request=request)

@router.post("/refresh", response_model=RefreshTokenResponse, status_code=status.HTTP_200_OK)
def refresh_token(req: RefreshTokenRequest, request: Request, db: Session = Depends(get_db)):
    """
    UC-009: Session Refresh & Access Token Renewal
    Validates active refresh token, checks user account status, and issues a new access token and rotating refresh token.
    """
    return AuthService.refresh_token(db, req, request=request)

@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
def logout(req: LogoutRequest, request: Request, db: Session = Depends(get_db)):
    """
    UC-010: User Sign Out & Token Revocation
    Revokes the provided refresh token server-side and logs a USER_LOGOUT audit event.
    """
    return AuthService.logout(db, req, request=request)




