try:
    import jwt
except ImportError:
    from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request, status
from app.core.config import settings
from app.models.user import User, utc_now
from app.models.organization import Organization
from app.models.user_organization import UserOrganization
from app.models.audit_log import AuditLog
from app.models.revoked_token import RevokedToken
from app.models.user_session import UserSession
from app.services.audit_service import AuditService

from app.schemas.auth import (
    RegisterRequest, GoogleRegisterRequest, LoginRequest, UserDTO, OrganizationDTO, AuthSessionDTO,
    ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse,
    RefreshTokenRequest, RefreshTokenResponse, LogoutRequest, LogoutResponse
)
from app.schemas.session import UserSessionDTO, SessionRevokeResponse

import re
import hashlib

def hash_password(password: str) -> str:
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    except Exception:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if pwd_context.verify(plain_password, hashed_password):
            return True
    except Exception:
        pass
    return hashlib.sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password

def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

class AuthService:
    @staticmethod
    def register_or_login(db: Session, req: RegisterRequest, request: Optional[Request] = None) -> AuthSessionDTO:
        provider = req.auth_provider or "google"

        if provider in ["google", "facebook"]:
            if not req.id_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="INVALID_AUTH_TOKEN"
                )
            if provider == "facebook" and not req.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="EMAIL_REQUIRED: Facebook permission denied for email or email not provided."
                )

        if provider == "email":
            if not req.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="EMAIL_REQUIRED: Email is required for email registration."
                )
            if not req.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="PASSWORD_REQUIRED: Password is required for email registration."
                )
            if len(req.password) < 8 or not re.search(r"[A-Z]", req.password) or not re.search(r"\d", req.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="WEAK_PASSWORD: Password must be at least 8 characters long, contain at least one uppercase letter and one digit."
                )

        password_hash = hash_password(req.password) if req.password else None

        if req.firebase_uid:
            firebase_uid = req.firebase_uid
        elif req.id_token:
            firebase_uid = f"{provider}-uid-{hash(req.id_token) % 1000000}"
        elif req.email:
            firebase_uid = f"email-uid-{abs(hash(req.email)) % 1000000}"
        else:
            firebase_uid = f"email-uid-{provider}"

        email = req.email or f"{firebase_uid}@example.com"
        full_name = req.full_name or (email.split("@")[0].capitalize() if provider == "email" else f"{provider.capitalize()} User")
        photo_url = req.photo_url

        # Check existing user by firebase_uid or email
        user = db.query(User).filter(
            (User.firebase_uid == firebase_uid) | (User.email == email)
        ).first()

        is_new_user = False

        if user:
            # Account Linking Flow (A1): Attach provider to linked_providers list if not present
            current_providers = list(user.linked_providers) if user.linked_providers else []
            if provider not in current_providers:
                current_providers.append(provider)
                user.linked_providers = current_providers
            if password_hash and not user.password_hash:
                user.password_hash = password_hash
            db.add(user)
            db.commit()
            db.refresh(user)

            # Existing User Flow: Fetch primary organization
            org = db.query(Organization).filter(
                Organization.owner_id == user.id,
                Organization.deleted_at == None
            ).first()

            if not org:
                org = Organization(
                    name=f"{user.full_name or 'User'}'s Personal Org",
                    owner_id=user.id,
                    is_personal=True,
                    max_vehicles=3,
                    max_drivers=3
                )
                db.add(org)
                db.flush()
                user_org = UserOrganization(
                    user_id=user.id,
                    organization_id=org.id,
                    role="owner",
                    status="active"
                )
                db.add(user_org)
                db.commit()
                db.refresh(org)
        else:
            is_new_user = True
            # New User Flow: Single Transaction Creation of User + Personal Org
            try:
                user = User(
                    firebase_uid=firebase_uid,
                    email=email,
                    full_name=full_name,
                    photo_url=photo_url,
                    auth_provider=provider,
                    linked_providers=[provider],
                    password_hash=password_hash
                )
                db.add(user)
                db.flush()  # Generate user.id within current transaction

                org = Organization(
                    name=f"{full_name}'s Personal Org",
                    owner_id=user.id,
                    is_personal=True,
                    max_vehicles=3,
                    max_drivers=3
                )
                db.add(org)
                db.flush()
                user_org = UserOrganization(
                    user_id=user.id,
                    organization_id=org.id,
                    role="owner",
                    status="active"
                )
                db.add(user_org)
                db.commit()
                db.refresh(user)
                db.refresh(org)

            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to provision user and organization: {str(e)}"
                )

        # UC-012: Audit Log Event Creation
        action = "USER_REGISTER" if is_new_user else "USER_LOGIN_SUCCESS"
        AuditService.log_event(
            db,
            action=action,
            actor_id=user.id,
            organization_id=org.id if org else None,
            payload={"auth_provider": provider, "email": user.email},
            request=request
        )
        db.commit()

        access_token = create_jwt_token(
            {"sub": user.id, "email": user.email, "org_id": org.id},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_jwt_token(
            {"sub": user.id, "type": "refresh"},
            timedelta(days=30)
        )

        AuthService._record_user_session(db, user.id, refresh_token, request=request)
        db.commit()

        return AuthSessionDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserDTO.model_validate(user),
            organization=OrganizationDTO.model_validate(org)
        )

    @staticmethod
    def _record_user_session(db: Session, user_id: str, refresh_token: str, request: Optional[Request] = None) -> UserSession:
        ip_address = "127.0.0.1"
        user_agent = "Unknown"
        if request is not None:
            if hasattr(request, "headers") and "x-forwarded-for" in request.headers:
                ip_address = request.headers["x-forwarded-for"].split(",")[0].strip()
            elif hasattr(request, "client") and request.client and getattr(request.client, "host", None):
                ip_address = request.client.host

            if hasattr(request, "headers") and "user-agent" in request.headers:
                user_agent = request.headers.get("user-agent", "Unknown")

        device_model = "Mobile Client" if ("Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent) else "Web App"
        os_name = "Android/iOS" if ("Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent) else "Desktop Browser"

        user_session = UserSession(
            user_id=user_id,
            refresh_token=refresh_token,
            device_model=device_model,
            os_name=os_name,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(user_session)
        db.flush()
        return user_session

    @staticmethod
    def register_or_login_google(db: Session, req: RegisterRequest, request: Optional[Request] = None) -> AuthSessionDTO:
        return AuthService.register_or_login(db, req, request=request)

    @staticmethod
    def login(db: Session, req: LoginRequest, request: Optional[Request] = None) -> AuthSessionDTO:
        user = db.query(User).filter(User.email == req.email).first()
        if not user:
            AuditService.log_event(
                db,
                action="USER_LOGIN_FAILURE",
                actor_id=None,
                payload={"email": req.email, "reason": "USER_NOT_FOUND"},
                request=request
            )
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_CREDENTIALS: User not found or incorrect password."
            )

        # Alternate Flow A1: Disabled user account or soft-deleted user
        if user.deleted_at is not None or getattr(user, "is_active", True) is False:
            AuditService.log_event(
                db,
                action="USER_LOGIN_FAILURE",
                actor_id=user.id,
                payload={"email": req.email, "reason": "USER_DISABLED"},
                request=request
            )
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="USER_DISABLED: User account is disabled or deleted."
            )

        # Edge Case: Password verification
        if not user.password_hash or not verify_password(req.password, user.password_hash):
            AuditService.log_event(
                db,
                action="USER_LOGIN_FAILURE",
                actor_id=user.id,
                payload={"email": req.email, "reason": "INVALID_PASSWORD"},
                request=request
            )
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_CREDENTIALS: User not found or incorrect password."
            )

        org = db.query(Organization).filter(
            Organization.owner_id == user.id,
            Organization.deleted_at == None
        ).first()

        if not org:
            org = Organization(
                name=f"{user.full_name or 'User'}'s Personal Org",
                owner_id=user.id,
                is_personal=True,
                max_vehicles=3,
                max_drivers=3
            )
            db.add(org)
            db.commit()
            db.refresh(org)

        # UC-012 Audit Log: Successful login
        AuditService.log_event(
            db,
            action="USER_LOGIN_SUCCESS",
            actor_id=user.id,
            organization_id=org.id if org else None,
            payload={"email": user.email},
            request=request
        )
        db.commit()

        access_token = create_jwt_token(
            {"sub": user.id, "email": user.email, "org_id": org.id},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_jwt_token(
            {"sub": user.id, "type": "refresh"},
            timedelta(days=30)
        )

        AuthService._record_user_session(db, user.id, refresh_token, request=request)
        db.commit()

        return AuthSessionDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserDTO.model_validate(user),
            organization=OrganizationDTO.model_validate(org)
        )

    @staticmethod
    def forgot_password(db: Session, req: ForgotPasswordRequest, request: Optional[Request] = None) -> ForgotPasswordResponse:
        user = db.query(User).filter(User.email == req.email).first()
        if not user or user.deleted_at is not None or getattr(user, "is_active", True) is False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="USER_NOT_FOUND"
            )

        reset_token = create_jwt_token(
            {"sub": user.id, "email": user.email, "type": "reset"},
            timedelta(minutes=5)
        )

        AuditService.log_event(
            db,
            action="USER_PASSWORD_RESET_REQUEST",
            actor_id=user.id,
            payload={"email": req.email},
            request=request
        )
        db.commit()

        return ForgotPasswordResponse(
            message="Password reset instructions have been generated.",
            reset_token=reset_token
        )

    @staticmethod
    def reset_password(db: Session, req: ResetPasswordRequest, request: Optional[Request] = None) -> ResetPasswordResponse:
        try:
            payload = jwt.decode(req.token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            if payload.get("type") != "reset":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="INVALID_TOKEN: Token type must be reset."
                )
            user_id = payload.get("sub")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="INVALID_TOKEN: Invalid or expired reset token."
            )

        new_password = req.new_password
        if len(new_password) < 8 or not re.search(r"[A-Z]", new_password) or not re.search(r"\d", new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="WEAK_PASSWORD: Password must be at least 8 characters long, contain at least one uppercase letter and one digit."
            )

        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.deleted_at is not None or getattr(user, "is_active", True) is False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="USER_NOT_FOUND"
            )

        user.password_hash = hash_password(new_password)
        db.add(user)

        AuditService.log_event(
            db,
            action="USER_PASSWORD_RESET_SUCCESS",
            actor_id=user.id,
            payload={"email": user.email},
            request=request
        )
        db.commit()

        return ResetPasswordResponse(
            message="Password has been successfully reset."
        )

    @staticmethod
    def refresh_token(db: Session, req: RefreshTokenRequest, request: Optional[Request] = None) -> RefreshTokenResponse:
        revoked = db.query(RevokedToken).filter(RevokedToken.token == req.refresh_token).first()
        if revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOKEN_REVOKED: Refresh token has been revoked."
            )

        session_entry = db.query(UserSession).filter(UserSession.refresh_token == req.refresh_token).first()
        if session_entry and session_entry.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOKEN_REVOKED: Refresh token session has been revoked."
            )

        try:
            payload = jwt.decode(req.refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="INVALID_REFRESH_TOKEN: Token type must be refresh."
                )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="INVALID_REFRESH_TOKEN: Missing user subject."
                )
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_REFRESH_TOKEN: Invalid or expired refresh token."
            )

        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.deleted_at is not None or getattr(user, "is_active", True) is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="USER_DISABLED: User account is disabled or deleted."
            )

        org = db.query(Organization).filter(
            Organization.owner_id == user.id,
            Organization.deleted_at == None
        ).first()

        if not org:
            org = Organization(
                name=f"{user.full_name or 'User'}'s Personal Org",
                owner_id=user.id,
                is_personal=True,
                max_vehicles=3,
                max_drivers=3
            )
            db.add(org)
            db.commit()
            db.refresh(org)

        access_token = create_jwt_token(
            {"sub": user.id, "email": user.email, "org_id": org.id},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        new_refresh_token = create_jwt_token(
            {"sub": user.id, "type": "refresh"},
            timedelta(days=30)
        )

        if session_entry:
            session_entry.refresh_token = new_refresh_token
            session_entry.last_active_at = utc_now()
            db.add(session_entry)
        else:
            AuthService._record_user_session(db, user.id, new_refresh_token, request=request)

        db.commit()

        return RefreshTokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token
        )

    @staticmethod
    def logout(db: Session, req: LogoutRequest, request: Optional[Request] = None) -> LogoutResponse:
        try:
            payload = jwt.decode(req.refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="INVALID_REFRESH_TOKEN: Token type must be refresh."
                )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="INVALID_REFRESH_TOKEN: Missing user subject."
                )
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_REFRESH_TOKEN: Invalid or expired refresh token."
            )

        existing = db.query(RevokedToken).filter(RevokedToken.token == req.refresh_token).first()
        if not existing:
            revoked = RevokedToken(
                token=req.refresh_token,
                user_id=user_id
            )
            db.add(revoked)

            AuditService.log_event(
                db,
                action="USER_LOGOUT",
                actor_id=user_id,
                payload={"refresh_token_revoked": True},
                request=request
            )
            db.commit()

        return LogoutResponse(
            message="Successfully logged out and token revoked."
        )

    @staticmethod
    def delete_account(db: Session, current_user: User, request: Optional[Request] = None) -> dict:
        """
        UC-011: Account Deletion (GDPR Right to be Forgotten)
        Soft-deletes user record, anonymizes PII, checks sole-owner status, and logs audit event.
        """
        owned_non_personal_orgs = db.query(Organization).filter(
            Organization.owner_id == current_user.id,
            Organization.is_personal == False,
            Organization.deleted_at == None
        ).all()

        for org in owned_non_personal_orgs:
            active_member_count = db.query(UserOrganization).filter(
                UserOrganization.organization_id == org.id,
                UserOrganization.status == "active"
            ).count()
            if active_member_count > 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="SOLE_OWNER_BLOCK: You are the sole owner of an active organization with active members. Please transfer ownership or delete the organization first."
                )

        current_user.deleted_at = utc_now()
        current_user.is_active = False
        current_user.email = f"deleted_{current_user.id}@anonymized.local"
        current_user.full_name = "Deleted User"
        current_user.phone_number = None
        current_user.city = None
        current_user.job_role = None
        current_user.photo_url = None
        current_user.avatar_url = None
        current_user.firebase_uid = f"deleted_{current_user.id}"

        db.add(current_user)

        AuditService.log_event(
            db,
            action="USER_ACCOUNT_DELETED",
            actor_id=current_user.id,
            payload={
                "user_id": current_user.id,
                "anonymized_at": utc_now().isoformat()
            },
            request=request
        )
        db.commit()

        return {"message": "Account successfully deleted and anonymized."}

    @staticmethod
    def get_user_sessions(db: Session, user_id: str, current_token: Optional[str] = None) -> list:
        sessions = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_revoked == False
        ).order_by(UserSession.last_active_at.desc()).all()

        results = []
        for s in sessions:
            dto = UserSessionDTO(
                id=s.id,
                user_id=s.user_id,
                device_model=s.device_model or "Unknown Device",
                os_name=s.os_name or "Unknown OS",
                ip_address=s.ip_address or "127.0.0.1",
                user_agent=s.user_agent or "Unknown",
                last_active_at=s.last_active_at,
                created_at=s.created_at,
                is_current=(s.refresh_token == current_token) if current_token else False
            )
            results.append(dto)
        return results

    @staticmethod
    def revoke_user_session(db: Session, user_id: str, session_id: str) -> SessionRevokeResponse:
        session_entry = db.query(UserSession).filter(
            UserSession.id == session_id,
            UserSession.user_id == user_id
        ).first()

        if not session_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SESSION_NOT_FOUND: Target session does not exist."
            )

        session_entry.is_revoked = True
        db.add(session_entry)

        revoked = db.query(RevokedToken).filter(RevokedToken.token == session_entry.refresh_token).first()
        if not revoked:
            db.add(RevokedToken(token=session_entry.refresh_token, user_id=user_id))

        AuditService.log_event(
            db,
            action="USER_SESSION_REVOKED",
            actor_id=user_id,
            payload={"revoked_session_id": session_id}
        )
        db.commit()

        return SessionRevokeResponse(
            message="Session successfully revoked.",
            revoked_session_id=session_id,
            revoked_count=1
        )

    @staticmethod
    def revoke_all_other_sessions(db: Session, user_id: str, current_token: Optional[str] = None) -> SessionRevokeResponse:
        query = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_revoked == False
        )
        if current_token:
            query = query.filter(UserSession.refresh_token != current_token)

        active_sessions = query.all()

        count = 0
        for s in active_sessions:
            s.is_revoked = True
            db.add(s)
            revoked = db.query(RevokedToken).filter(RevokedToken.token == s.refresh_token).first()
            if not revoked:
                db.add(RevokedToken(token=s.refresh_token, user_id=user_id))
            count += 1

        AuditService.log_event(
            db,
            action="USER_ALL_OTHER_SESSIONS_REVOKED",
            actor_id=user_id,
            payload={"revoked_count": count}
        )
        db.commit()

        return SessionRevokeResponse(
            message="All other active sessions revoked.",
            revoked_count=count
        )







