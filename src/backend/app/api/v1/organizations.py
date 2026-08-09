import secrets
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.organization_invitation import OrganizationInvitation
from app.schemas.organization import (
    OrganizationCreate,
    PersonalOrganizationCreate,
    OrganizationResponse,
    SwitchOrganizationRequest,
    SwitchOrganizationResponse,
)
from app.schemas.organization_invitation import (
    OrganizationInvitationCreate,
    OrganizationInvitationResponse,
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    payload: OrganizationCreate,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-014: Provision commercial or custom organization.
    """
    owner_id = payload.owner_id or x_user_id

    if owner_id:
        user = db.query(User).filter(User.id == owner_id, User.deleted_at == None).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Owner user not found"
            )

    org = Organization(
        name=payload.name,
        owner_id=owner_id,
        is_personal=payload.is_personal,
        max_vehicles=payload.max_vehicles,
        max_drivers=payload.max_drivers
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@router.post("/personal", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def auto_create_personal_organization(
    payload: PersonalOrganizationCreate,
    db: Session = Depends(get_db)
):
    """
    UC-014: Auto-provision personal organization for a user during registration or setup.
    """
    user = db.query(User).filter(User.id == payload.user_id, User.deleted_at == None).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Return existing personal org if already provisioned
    existing_org = db.query(Organization).filter(
        Organization.owner_id == payload.user_id,
        Organization.is_personal == True,
        Organization.deleted_at == None
    ).first()

    if existing_org:
        return existing_org

    display_name = payload.user_name or user.full_name or "User"
    org_name = f"{display_name}'s Personal Org"

    org = Organization(
        name=org_name,
        owner_id=user.id,
        is_personal=True,
        max_vehicles=3,
        max_drivers=3
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@router.get("", response_model=List[OrganizationResponse])
def get_organizations(
    user_id: Optional[str] = Query(None, description="Filter organizations by owner user ID"),
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve organizations list.
    """
    target_user_id = user_id or x_user_id

    query = db.query(Organization).filter(Organization.deleted_at == None)
    if target_user_id:
        query = query.filter(Organization.owner_id == target_user_id)

    return query.all()

@router.post("/switch", response_model=SwitchOrganizationResponse)
def switch_organization_context(
    payload: SwitchOrganizationRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-015: Switch active organization context for user.
    """
    user_id = payload.user_id or x_user_id

    org = db.query(Organization).filter(
        Organization.id == payload.target_organization_id,
        Organization.deleted_at == None
    ).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    if not user_id or org.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to target organization"
        )

    return SwitchOrganizationResponse(
        message="Active organization switched successfully",
        active_organization=OrganizationResponse.model_validate(org)
    )

@router.get("/active", response_model=OrganizationResponse)
def get_active_organization(
    user_id: Optional[str] = Query(None, description="User ID"),
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-015: Get active organization for user.
    """
    target_user_id = user_id or x_user_id

    if not target_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active organization not found"
        )

    org = db.query(Organization).filter(
        Organization.owner_id == target_user_id,
        Organization.deleted_at == None
    ).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active organization not found"
        )

    return org

@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization_by_id(
    organization_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve organization details by ID.
    """
    org = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at == None
    ).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    return org

@router.post("/{organization_id}/invitations", response_model=OrganizationInvitationResponse, status_code=status.HTTP_201_CREATED)
def create_organization_invitation(
    organization_id: str,
    payload: OrganizationInvitationCreate,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-016: Invite Team Member to Organization.
    Generates a secure 64-character token with 7-day TTL.
    """
    org = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at == None
    ).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    if not x_user_id or org.owner_id != x_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to manage invitations for this organization"
        )

    token = secrets.token_hex(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    existing_invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.organization_id == organization_id,
        OrganizationInvitation.email == payload.email,
        OrganizationInvitation.status == "PENDING"
    ).first()

    if existing_invitation:
        existing_invitation.token = token
        existing_invitation.role = payload.role
        existing_invitation.expires_at = expires_at
        existing_invitation.updated_at = datetime.now(timezone.utc)
        invitation = existing_invitation
    else:
        invitation = OrganizationInvitation(
            organization_id=organization_id,
            email=payload.email,
            role=payload.role,
            token=token,
            status="PENDING",
            invited_by_user_id=x_user_id,
            expires_at=expires_at
        )
        db.add(invitation)

    db.commit()
    db.refresh(invitation)
    return invitation

@router.get("/{organization_id}/invitations", response_model=List[OrganizationInvitationResponse])
def get_organization_invitations(
    organization_id: str,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-016: List pending organization invitations.
    """
    org = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at == None
    ).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    if not x_user_id or org.owner_id != x_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to view invitations for this organization"
        )

    invitations = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.organization_id == organization_id
    ).all()

    return invitations

