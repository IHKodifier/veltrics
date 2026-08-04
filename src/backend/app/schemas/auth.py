from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

class GoogleRegisterRequest(BaseModel):
    id_token: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    photo_url: Optional[str] = None
    firebase_uid: Optional[str] = None

class UserDTO(BaseModel):
    id: str
    firebase_uid: str
    email: str
    full_name: Optional[str] = None
    photo_url: Optional[str] = None
    auth_provider: str
    linked_providers: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class OrganizationDTO(BaseModel):
    id: str
    name: str
    owner_id: str
    is_personal: bool
    max_vehicles: int
    max_drivers: int

    model_config = ConfigDict(from_attributes=True)

class AuthSessionDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserDTO
    organization: OrganizationDTO
