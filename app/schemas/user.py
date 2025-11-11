from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserResponse(BaseModel):
    """Schema for returning user data in responses"""
    id: UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Allow ORM object mapping


class Token(BaseModel):
    """Schema for token response during authentication"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "987f6543-e21b-45c7-a123-789456123000",
                    "username": "alicesmith",
                    "email": "alice.smith@email.com",
                    "first_name": "Alice",
                    "last_name": "Smith",
                    "is_active": True,
                    "is_verified": False,
                    "created_at": "2025-01-15T08:30:00",
                    "updated_at": "2025-01-20T14:45:00",
                },
            }
        }
    )


class TokenData(BaseModel):
    """Schema for decoded JWT token payload data"""
    user_id: Optional[UUID] = None


class UserLogin(BaseModel):
    """Schema for user authentication credentials"""
    username: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "alicesmith",
                "password": "MyPass456",
            }
        }
    )