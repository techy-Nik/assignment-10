from pydantic import BaseModel, EmailStr, Field, ConfigDict, ValidationError, model_validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class BaseUserSchema(BaseModel):
    """Core user schema containing shared attributes"""
    first_name: str = Field(max_length=50, example="Alice")
    last_name: str = Field(max_length=50, example="Smith")
    email: EmailStr = Field(example="alice.smith@email.com")
    username: str = Field(min_length=3, max_length=50, example="alicesmith")

    model_config = ConfigDict(from_attributes=True)


class SecurePasswordValidator(BaseModel):
    """Validator mixin for enforcing password security rules"""
    password: str = Field(min_length=6, max_length=128, example="MyPass456")

    @model_validator(mode="before")
    @classmethod
    def check_password_strength(cls, data: dict) -> dict:
        pwd = data.get("password")
        if not pwd:
            raise ValidationError("Password is required", model=cls) # pragma: no cover
        if len(pwd) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if not any(c.isupper() for c in pwd):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in pwd):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in pwd):
            raise ValueError("Password must contain at least one digit")
        return data


class UserCreate(BaseUserSchema, SecurePasswordValidator):
    """Schema for creating new user accounts"""
    pass


class UserLogin(SecurePasswordValidator):
    """Schema for authenticating existing users"""
    username: str = Field(
        description="Username or email",
        min_length=3,
        max_length=50,
        example="alicesmith"
    )