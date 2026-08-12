from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

class RegisterRequest(BaseModel):
    id_token: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    photo_url: Optional[str] = None
    firebase_uid: Optional[str] = None
    auth_provider: str = "google"

# Alias for backwards compatibility
GoogleRegisterRequest = RegisterRequest

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    id_token: Optional[str] = None
    firebase_uid: Optional[str] = None

class UserDTO(BaseModel):
    id: str
    firebase_uid: str
    email: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    job_role: Optional[str] = None
    photo_url: Optional[str] = None
    avatar_url: Optional[str] = None
    auth_provider: str
    linked_providers: List[str] = []
    is_super_admin: bool = False

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

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordResponse(BaseModel):
    message: str
    reset_token: Optional[str] = None

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class ResetPasswordResponse(BaseModel):
    message: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LogoutRequest(BaseModel):
    refresh_token: str

class LogoutResponse(BaseModel):
    message: str = "Successfully logged out and token revoked."



