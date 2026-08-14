import secrets
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.organization_invitation import OrganizationInvitation
from app.models.user_organization import UserOrganization
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.fuel_log import FuelLog
from app.models.trip import Trip
from app.models.expense_log import ExpenseLog
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
from app.models.audit_log import AuditLog

from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
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

def check_org_admin_permission(org: Organization, user_id: Optional[str], db: Session) -> bool:
    if not user_id:
        return False
    if org.owner_id == user_id:
        return True
    membership = db.query(UserOrganization).filter(
        UserOrganization.organization_id == org.id,
        UserOrganization.user_id == user_id,
        UserOrganization.status == "active"
    ).first()
    if membership and membership.role in ["owner", "admin"]:
        return True
    return False

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

    if owner_id:
        member = UserOrganization(
            user_id=owner_id,
            organization_id=org.id,
            role="owner",
            status="active"
        )
        db.add(member)
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

    member = UserOrganization(
        user_id=user.id,
        organization_id=org.id,
        role="owner",
        status="active"
    )
    db.add(member)
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

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to target organization"
        )

    is_owner = org.owner_id == user_id
    is_member = db.query(UserOrganization).filter(
        UserOrganization.organization_id == org.id,
        UserOrganization.user_id == user_id,
        UserOrganization.status == "active"
    ).first() is not None

    if not (is_owner or is_member):
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
        membership = db.query(UserOrganization).filter(
            UserOrganization.user_id == target_user_id,
            UserOrganization.status == "active"
        ).first()
        if membership:
            org = db.query(Organization).filter(
                Organization.id == membership.organization_id,
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

@router.patch("/{organization_id}", response_model=OrganizationResponse)
def update_organization_profile(
    organization_id: str,
    payload: OrganizationUpdate,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-017: Edit Organization Profile Details.
    Enforces ISO 4217 currency validation, owner/admin check, and audit logging.
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

    if not check_org_admin_permission(org, x_user_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to modify this organization"
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(org, field, value)

    org.updated_at = datetime.now(timezone.utc)

    audit_log = AuditLog(
        organization_id=org.id,
        actor_id=x_user_id,
        action="EDIT_ORGANIZATION_PROFILE",
        payload={"target_entity": "organizations", "target_id": org.id, "updates": update_data}
    )
    db.add(audit_log)

    db.commit()
    db.refresh(org)
    return org

@router.post("/{organization_id}/invitations", response_model=OrganizationInvitationResponse, status_code=status.HTTP_201_CREATED)
def create_organization_invitation(
    organization_id: str,
    payload: OrganizationInvitationCreate,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-018: Invite Driver / Manager via Email or Phone.
    Generates a secure 64-character token with 7-day TTL. Updates existing pending invitation if re-invited.
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

    if not check_org_admin_permission(org, x_user_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to manage invitations for this organization"
        )

    if not payload.email and not payload.phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide email or phone for invitation"
        )

    token = secrets.token_hex(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    query = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.organization_id == organization_id,
        OrganizationInvitation.status == "PENDING"
    )
    if payload.email:
        query = query.filter(OrganizationInvitation.email == payload.email)
    elif payload.phone:
        query = query.filter(OrganizationInvitation.phone == payload.phone)

    existing_invitation = query.first()

    if existing_invitation:
        existing_invitation.token = token
        existing_invitation.role = payload.role
        existing_invitation.expires_at = expires_at
        existing_invitation.updated_at = datetime.now(timezone.utc)
        if payload.email:
            existing_invitation.email = payload.email
        if payload.phone:
            existing_invitation.phone = payload.phone
        invitation = existing_invitation
    else:
        invitation = OrganizationInvitation(
            organization_id=organization_id,
            email=payload.email,
            phone=payload.phone,
            role=payload.role,
            token=token,
            status="PENDING",
            invited_by_user_id=x_user_id,
            expires_at=expires_at
        )
        db.add(invitation)

    audit_log = AuditLog(
        organization_id=org.id,
        actor_id=x_user_id,
        action="INVITE_ORG_MEMBER",
        payload={"target_entity": "organization_invitations", "target_id": organization_id, "recipient": payload.email or payload.phone, "role": payload.role}
    )
    db.add(audit_log)

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
    UC-018: List pending organization invitations.
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

    if not check_org_admin_permission(org, x_user_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to view invitations for this organization"
        )

    invitations = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.organization_id == organization_id
    ).all()

    return invitations

@router.delete("/{organization_id}/members/{user_id}")
def remove_organization_member(
    organization_id: str,
    user_id: str,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-021: Remove Member from Organization.
    Prevents owner removal. Unassigns user from vehicles.
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

    if org.owner_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove organization owner"
        )

    is_self = x_user_id == user_id
    is_admin = check_org_admin_permission(org, x_user_id, db)
    if not (is_self or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have authority to remove this member"
        )

    membership = db.query(UserOrganization).filter(
        UserOrganization.organization_id == organization_id,
        UserOrganization.user_id == user_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not a member of this organization"
        )

    db.delete(membership)

    drivers = db.query(Driver).filter(
        Driver.organization_id == organization_id,
        Driver.user_id == user_id
    ).all()
    driver_ids = [d.id for d in drivers] + [user_id]

    vehicles = db.query(Vehicle).filter(
        Vehicle.organization_id == organization_id,
        Vehicle.assigned_driver_id.in_(driver_ids)
    ).all()
    for v in vehicles:
        v.assigned_driver_id = None

    audit_log = AuditLog(
        organization_id=organization_id,
        actor_id=x_user_id,
        action="REMOVE_ORG_MEMBER",
        payload={"target_entity": "user_organizations", "target_id": user_id, "removed_user_id": user_id}
    )
    db.add(audit_log)

    db.commit()
    return {"message": "Member removed successfully"}

@router.delete("/{organization_id}/invitations/{invitation_id}")
def cancel_organization_invitation(
    organization_id: str,
    invitation_id: str,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-022: Cancel Pending Member Invitation.
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

    if not check_org_admin_permission(org, x_user_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to cancel invitations for this organization"
        )

    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.id == invitation_id,
        OrganizationInvitation.organization_id == organization_id
    ).first()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found"
        )

    invitation.status = "REVOKED"
    invitation.updated_at = datetime.now(timezone.utc)

    audit_log = AuditLog(
        organization_id=organization_id,
        actor_id=x_user_id,
        action="CANCEL_ORG_INVITATION",
        payload={"target_entity": "organization_invitations", "target_id": invitation_id}
    )
    db.add(audit_log)

    db.commit()
    return {"message": "Invitation cancelled successfully"}

@router.delete("/{organization_id}")
def soft_delete_organization(
    organization_id: str,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    db: Session = Depends(get_db)
):
    """
    UC-023: Soft Delete Organization & Child Entities.
    Rejects personal org deletion with HTTP 400 Bad Request.
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

    if org.is_personal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Personal organization cannot be deleted"
        )

    if not x_user_id or org.owner_id != x_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization owner can delete the organization"
        )

    now = datetime.now(timezone.utc)
    org.deleted_at = now

    db.query(Vehicle).filter(Vehicle.organization_id == organization_id, Vehicle.deleted_at == None).update({"deleted_at": now}, synchronize_session=False)
    db.query(Driver).filter(Driver.organization_id == organization_id, Driver.deleted_at == None).update({"deleted_at": now}, synchronize_session=False)
    db.query(FuelLog).filter(FuelLog.organization_id == organization_id, FuelLog.deleted_at == None).update({"deleted_at": now}, synchronize_session=False)
    db.query(Trip).filter(Trip.organization_id == organization_id, Trip.deleted_at == None).update({"deleted_at": now}, synchronize_session=False)
    db.query(ExpenseLog).filter(ExpenseLog.organization_id == organization_id, ExpenseLog.deleted_at == None).update({"deleted_at": now}, synchronize_session=False)
    db.query(MaintenanceSchedule).filter(MaintenanceSchedule.organization_id == organization_id, MaintenanceSchedule.deleted_at == None).update({"deleted_at": now}, synchronize_session=False)
    db.query(ServiceRecord).filter(ServiceRecord.organization_id == organization_id, ServiceRecord.deleted_at == None).update({"deleted_at": now}, synchronize_session=False)

    audit_log = AuditLog(
        organization_id=organization_id,
        actor_id=x_user_id,
        action="DELETE_ORGANIZATION",
        payload={"target_entity": "organizations", "target_id": organization_id}
    )
    db.add(audit_log)

    db.commit()
    return {"message": "Organization soft-deleted successfully"}
