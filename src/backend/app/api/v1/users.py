from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user, require_organization_role
from app.models.user import User
from app.models.organization import Organization
from app.schemas.user import UserProfileUpdate, ProfileCompletionRequest, UserProfileResponse
from app.schemas.auth import AuthSessionDTO, UserDTO, OrganizationDTO
from app.services.auth_service import create_jwt_token, timedelta

router = APIRouter(prefix="/users", tags=["User Profiles"])

@router.get("/me", response_model=UserProfileResponse, status_code=status.HTTP_200_OK)
def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    UC-007: Fetch current user profile details.
    """
    return UserProfileResponse(
        id=current_user.id,
        firebase_uid=current_user.firebase_uid,
        email=current_user.email,
        full_name=current_user.full_name,
        phone_number=current_user.phone_number,
        city=current_user.city,
        job_role=current_user.job_role,
        photo_url=current_user.photo_url or current_user.avatar_url,
        avatar_url=current_user.avatar_url or current_user.photo_url,
        auth_provider=current_user.auth_provider,
        linked_providers=current_user.linked_providers or [],
        is_super_admin=current_user.is_super_admin or False,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.patch("/me", response_model=UserProfileResponse, status_code=status.HTTP_200_OK)
def update_user_profile(
    payload: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    UC-007: Update current user profile (full name, phone, city, job role, avatar).
    """
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.phone_number is not None:
        current_user.phone_number = payload.phone_number
    if payload.city is not None:
        current_user.city = payload.city
    if payload.job_role is not None:
        current_user.job_role = payload.job_role
    if payload.avatar_url is not None:
        current_user.avatar_url = payload.avatar_url
        current_user.photo_url = payload.avatar_url

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return UserProfileResponse(
        id=current_user.id,
        firebase_uid=current_user.firebase_uid,
        email=current_user.email,
        full_name=current_user.full_name,
        phone_number=current_user.phone_number,
        city=current_user.city,
        job_role=current_user.job_role,
        photo_url=current_user.photo_url or current_user.avatar_url,
        avatar_url=current_user.avatar_url or current_user.photo_url,
        auth_provider=current_user.auth_provider,
        linked_providers=current_user.linked_providers or [],
        is_super_admin=current_user.is_super_admin or False,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.post("/me/complete-profile", response_model=AuthSessionDTO, status_code=status.HTTP_200_OK)
def complete_profile(
    payload: ProfileCompletionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    UC-007: Complete profile onboarding (SCR-AUTH-007) and return updated AuthSessionDTO.
    """
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.phone_number is not None:
        current_user.phone_number = payload.phone_number
    if payload.city is not None:
        current_user.city = payload.city
    if payload.job_role is not None:
        current_user.job_role = payload.job_role
    if payload.avatar_url is not None:
        current_user.avatar_url = payload.avatar_url
        current_user.photo_url = payload.avatar_url

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    # Fetch active or personal organization
    org = db.query(Organization).filter(
        Organization.owner_id == current_user.id,
        Organization.deleted_at == None
    ).first()

    if not org:
        # Fallback to auto-create personal organization
        org = Organization(
            name=f"{current_user.full_name or 'User'}'s Personal Org",
            owner_id=current_user.id,
            is_personal=True,
            max_vehicles=3,
            max_drivers=3
        )
        db.add(org)
        db.commit()
        db.refresh(org)

    access_token = create_jwt_token({"sub": current_user.id, "email": current_user.email}, timedelta(minutes=1440))
    refresh_token = create_jwt_token({"sub": current_user.id, "type": "refresh"}, timedelta(days=30))

    user_dto = UserDTO(
        id=current_user.id,
        firebase_uid=current_user.firebase_uid,
        email=current_user.email,
        full_name=current_user.full_name,
        phone_number=current_user.phone_number,
        city=current_user.city,
        job_role=current_user.job_role,
        photo_url=current_user.photo_url or current_user.avatar_url,
        avatar_url=current_user.avatar_url or current_user.photo_url,
        auth_provider=current_user.auth_provider,
        linked_providers=current_user.linked_providers or [],
        is_super_admin=current_user.is_super_admin or False
    )

    org_dto = OrganizationDTO(
        id=org.id,
        name=org.name,
        owner_id=org.owner_id or current_user.id,
        is_personal=org.is_personal,
        max_vehicles=org.max_vehicles,
        max_drivers=org.max_drivers
    )

    return AuthSessionDTO(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user_dto,
        organization=org_dto
    )

@router.get("/me/tenant-check", status_code=status.HTTP_200_OK)
def tenant_role_check(
    tenant_context: dict = Depends(require_organization_role())
):
    """
    UC-007: Multi-tenant authorization boundary verification endpoint.
    """
    return {
        "status": "ok",
        "role": tenant_context["role"],
        "organization_id": tenant_context["organization"].id,
        "user_id": tenant_context["user"].id
    }
