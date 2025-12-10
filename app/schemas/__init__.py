"""Pydantic schemas for user data validation and serialization."""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    Used when registering a new user account.
    """
    username: str = Field(..., min_length=3, max_length=50, description="Username for the account")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password (minimum 8 characters)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "securepassword123"
            }
        }
    )


class UserRead(BaseModel):
    """
    Schema for reading user data.
    Returns user information without exposing the password hash.
    """
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "johndoe@example.com",
                "created_at": "2024-01-01T12:00:00Z"
            }
        }
    )


class UserUpdate(BaseModel):
    """
    Schema for updating user information.
    All fields are optional.
    """
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "newemail@example.com"
            }
        }
    )


class UserProfileUpdate(BaseModel):
    """Schema for profile updates (username/email)."""

    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "newusername",
                "email": "newemail@example.com"
            }
        }
    )


class PasswordChange(BaseModel):
    """Schema for password change requests."""

    current_password: str = Field(..., min_length=8, max_length=100)
    new_password: str = Field(..., min_length=8, max_length=100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_password": "oldpass123",
                "new_password": "newstrongpass456"
            }
        }
    )


class UserProfileResponse(BaseModel):
    """Response for profile updates with optional refreshed token."""

    user: "UserRead"
    access_token: str | None = None
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str


# Import calculation schemas
from app.schemas.calculation import (  # noqa: E402
    CalculationCreate,
    CalculationRead,
    CalculationUpdate,
    CalculationType
)

__all__ = [
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserLogin",
    "Token",
    "CalculationCreate",
    "CalculationRead",
    "CalculationUpdate",
    "CalculationType",
    "UserProfileUpdate",
    "PasswordChange",
    "UserProfileResponse"
]
