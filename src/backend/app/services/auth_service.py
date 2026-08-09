try:
    import jwt
except ImportError:
    from jose import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.config import settings
from app.models.user import User
from app.models.organization import Organization
from app.models.user_organization import UserOrganization

from app.schemas.auth import (
    RegisterRequest, GoogleRegisterRequest, LoginRequest, UserDTO, OrganizationDTO, AuthSessionDTO,
    ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse
)

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
    def register_or_login(db: Session, req: RegisterRequest) -> AuthSessionDTO:
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

        access_token = create_jwt_token(
            {"sub": user.id, "email": user.email, "org_id": org.id},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_jwt_token(
            {"sub": user.id, "type": "refresh"},
            timedelta(days=30)
        )

        return AuthSessionDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserDTO.model_validate(user),
            organization=OrganizationDTO.model_validate(org)
        )

    @staticmethod
    def register_or_login_google(db: Session, req: RegisterRequest) -> AuthSessionDTO:
        return AuthService.register_or_login(db, req)

    @staticmethod
    def login(db: Session, req: LoginRequest) -> AuthSessionDTO:
        user = db.query(User).filter(User.email == req.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_CREDENTIALS: User not found or incorrect password."
            )

        # Alternate Flow A1: Disabled user account or soft-deleted user
        if user.deleted_at is not None or getattr(user, "is_active", True) is False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="USER_DISABLED: User account is disabled or deleted."
            )

        # Edge Case: Password verification
        if not user.password_hash or not verify_password(req.password, user.password_hash):
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

        access_token = create_jwt_token(
            {"sub": user.id, "email": user.email, "org_id": org.id},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_jwt_token(
            {"sub": user.id, "type": "refresh"},
            timedelta(days=30)
        )

        return AuthSessionDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserDTO.model_validate(user),
            organization=OrganizationDTO.model_validate(org)
        )

    @staticmethod
    def forgot_password(db: Session, req: ForgotPasswordRequest) -> ForgotPasswordResponse:
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

        return ForgotPasswordResponse(
            message="Password reset instructions have been generated.",
            reset_token=reset_token
        )

    @staticmethod
    def reset_password(db: Session, req: ResetPasswordRequest) -> ResetPasswordResponse:
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
        db.commit()

        return ResetPasswordResponse(
            message="Password has been successfully reset."
        )


