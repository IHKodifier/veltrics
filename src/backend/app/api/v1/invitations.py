from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.organization_invitation import OrganizationInvitation
from app.models.user_organization import UserOrganization
from app.models.audit_log import AuditLog

from app.schemas.organization_invitation import (
    OrganizationInvitationResponse,
    OrganizationInvitationRedeem,
    RedeemInvitationResponse,
)

router = APIRouter(prefix="/invitations", tags=["Invitations"])

def is_expired(expires_at: Optional[datetime]) -> bool:
    if not expires_at:
        return False
    exp_naive = expires_at.replace(tzinfo=None) if expires_at.tzinfo else expires_at
    now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    return exp_naive < now_naive

@router.get("/{token}", response_model=OrganizationInvitationResponse)
def get_invitation_by_token(
    token: str,
    db: Session = Depends(get_db)
):
    """
    UC-019: Inspect / validate organization invitation token details.
    Returns HTTP 410 Gone if expired.
    """
    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.token == token
    ).first()

    if not invitation:
        invitation = db.query(OrganizationInvitation).filter(
            OrganizationInvitation.id == token
        ).first()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found"
        )

    if invitation.status != "PENDING" or is_expired(invitation.expires_at):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="INVITATION_EXPIRED"
        )

    return invitation

@router.post("/{token}/accept", response_model=RedeemInvitationResponse)
def accept_organization_invitation(
    token: str,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    UC-019: Accept Organization Invitation for existing authenticated user.
    """
    target_user_id = user_id or x_user_id
    if not target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required to accept invitation"
        )

    user = db.query(User).filter(User.id == target_user_id, User.deleted_at == None).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.token == token
    ).first()

    if not invitation:
        invitation = db.query(OrganizationInvitation).filter(
            OrganizationInvitation.id == token
        ).first()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found"
        )

    if invitation.status != "PENDING" or is_expired(invitation.expires_at):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="INVITATION_EXPIRED"
        )

    membership = db.query(UserOrganization).filter(
        UserOrganization.organization_id == invitation.organization_id,
        UserOrganization.user_id == target_user_id
    ).first()

    if membership:
        membership.role = invitation.role
        membership.status = "active"
    else:
        membership = UserOrganization(
            organization_id=invitation.organization_id,
            user_id=target_user_id,
            role=invitation.role,
            status="active"
        )
        db.add(membership)

    invitation.status = "ACCEPTED"
    invitation.updated_at = datetime.now(timezone.utc)

    audit_log = AuditLog(
        organization_id=invitation.organization_id,
        actor_id=target_user_id,
        action="ACCEPT_ORG_INVITATION",
        payload={"target_entity": "organization_invitations", "target_id": invitation.id}
    )
    db.add(audit_log)

    db.commit()
    return RedeemInvitationResponse(
        message="Invitation accepted successfully",
        organization_id=invitation.organization_id,
        role=invitation.role,
        status="active"
    )

@router.post("/redeem", response_model=RedeemInvitationResponse)
def redeem_organization_invitation_code(
    payload: OrganizationInvitationRedeem,
    db: Session = Depends(get_db)
):
    """
    UC-020: Redeem Org Invitation Code for new user during signup/onboard.
    """
    user = db.query(User).filter(User.id == payload.user_id, User.deleted_at == None).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.token == payload.invitation_code
    ).first()

    if not invitation:
        invitation = db.query(OrganizationInvitation).filter(
            OrganizationInvitation.id == payload.invitation_code
        ).first()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invitation code"
        )

    if invitation.status != "PENDING" or is_expired(invitation.expires_at):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="INVITATION_EXPIRED"
        )

    membership = db.query(UserOrganization).filter(
        UserOrganization.organization_id == invitation.organization_id,
        UserOrganization.user_id == payload.user_id
    ).first()

    if membership:
        membership.role = invitation.role
        membership.status = "active"
    else:
        membership = UserOrganization(
            organization_id=invitation.organization_id,
            user_id=payload.user_id,
            role=invitation.role,
            status="active"
        )
        db.add(membership)

    invitation.status = "ACCEPTED"
    invitation.updated_at = datetime.now(timezone.utc)

    audit_log = AuditLog(
        organization_id=invitation.organization_id,
        actor_id=payload.user_id,
        action="REDEEM_ORG_INVITATION",
        payload={"target_entity": "organization_invitations", "target_id": invitation.id}
    )
    db.add(audit_log)

    db.commit()
    return RedeemInvitationResponse(
        message="Invitation redeemed successfully",
        organization_id=invitation.organization_id,
        role=invitation.role,
        status="active"
    )
