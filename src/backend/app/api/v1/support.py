from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user_optional, get_current_user
from app.models.user import User
from app.models.support_ticket import SupportTicket
from app.schemas.support_ticket import SupportTicketCreate, SupportTicketResponse

router = APIRouter(prefix="/support", tags=["Support & Feedback"])

@router.post("/tickets", response_model=SupportTicketResponse, status_code=status.HTTP_201_CREATED)
def create_support_ticket(
    payload: SupportTicketCreate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    UC-117: Submit feedback or in-app support ticket.
    Auto-attaches user profile ID (if authenticated) and device metadata.
    """
    ticket = SupportTicket(
        user_id=current_user.id if current_user else None,
        category=payload.category,
        description=payload.description,
        device_info=payload.device_info or {},
        status="OPEN"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.get("/tickets", response_model=List[SupportTicketResponse], status_code=status.HTTP_200_OK)
def list_user_support_tickets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    UC-117: List support tickets submitted by current authenticated user.
    """
    tickets = db.query(SupportTicket).filter(
        SupportTicket.user_id == current_user.id
    ).order_by(SupportTicket.created_at.desc()).all()
    return tickets
