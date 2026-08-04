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
from app.schemas.auth import GoogleRegisterRequest, UserDTO, OrganizationDTO, AuthSessionDTO

def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

class AuthService:
    @staticmethod
    def register_or_login_google(db: Session, req: GoogleRegisterRequest) -> AuthSessionDTO:
        if not req.id_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_GOOGLE_TOKEN"
            )

        # In dev/emulator mode, mock token extraction or parse payload
        firebase_uid = req.firebase_uid or f"google-uid-{hash(req.id_token) % 1000000}"
        email = req.email or f"{firebase_uid}@example.com"
        full_name = req.full_name or "Google User"
        photo_url = req.photo_url

        # Check existing user
        user = db.query(User).filter(
            (User.firebase_uid == firebase_uid) | (User.email == email)
        ).first()

        if user:
            # Existing User Flow: Fetch primary organization
            org = db.query(Organization).filter(
                Organization.owner_id == user.id,
                Organization.deleted_at == None
            ).first()

            if not org:
                # Provision org if missing
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
        else:
            # New User Flow: Single Transaction Creation of User + Personal Org
            try:
                user = User(
                    firebase_uid=firebase_uid,
                    email=email,
                    full_name=full_name,
                    photo_url=photo_url,
                    auth_provider="google",
                    linked_providers=["google"]
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
