from typing import Optional, List, Callable
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
try:
    import jwt
except ImportError:
    from jose import jwt

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.user_organization import UserOrganization

def get_current_user(
    db: Session = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> User:
    user_id = None

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get("sub") or payload.get("user_id")
        except Exception:
            pass

    if not user_id and x_user_id:
        user_id = x_user_id

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="AUTHENTICATION_REQUIRED"
        )

    user = db.query(User).filter(User.id == user_id, User.deleted_at == None).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="USER_NOT_FOUND"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="USER_INACTIVE"
        )

    return user

def get_current_user_optional(
    db: Session = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> Optional[User]:
    try:
        return get_current_user(db=db, x_user_id=x_user_id, authorization=authorization)
    except HTTPException:
        return None

def require_organization_role(allowed_roles: Optional[List[str]] = None) -> Callable:
    def _checker(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")
    ):
        if not x_organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ORGANIZATION_HEADER_REQUIRED"
            )

        org = db.query(Organization).filter(
            Organization.id == x_organization_id,
            Organization.deleted_at == None
        ).first()

        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ORGANIZATION_NOT_FOUND"
            )

        # Owner has full access to their owned organization
        if org.owner_id == current_user.id:
            user_role = "owner"
        else:
            membership = db.query(UserOrganization).filter(
                UserOrganization.organization_id == x_organization_id,
                UserOrganization.user_id == current_user.id,
                UserOrganization.status == "active"
            ).first()

            if not membership:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="FORBIDDEN_ORGANIZATION_ACCESS: User is not an active member of this organization."
                )

            user_role = membership.role

        if allowed_roles:
            normalized_allowed = [r.lower() for r in allowed_roles]
            # Owner always passes role requirements unless explicitly excluded
            if user_role != "owner" and user_role.lower() not in normalized_allowed:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"INSUFFICIENT_ROLE_PERMISSIONS: Role '{user_role}' does not have required access ({allowed_roles})."
                )

        return {
            "user": current_user,
            "organization": org,
            "role": user_role
        }

    return _checker
