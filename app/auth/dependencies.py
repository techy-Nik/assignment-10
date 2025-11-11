# app/auth/user_validator.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.schemas.user import UserResponse

# Token authentication scheme
token_auth = OAuth2PasswordBearer(tokenUrl="token")

class AuthError(HTTPException):
    """Exception raised when authentication fails."""
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

def validate_user_from_token(
    db,
    auth_token: str = Depends(token_auth)
) -> UserResponse:
    """Validate and retrieve user from JWT token."""
    
    # Verify the provided token
    uid = User.verify_token(auth_token)
    if uid is None:
        raise AuthError()
    
    # Query database for user
    db_user = db.query(User).filter(User.id == uid).first()
    if db_user is None:
        raise AuthError()
        
    return UserResponse.model_validate(db_user)

def ensure_user_is_active(
    authenticated_user: UserResponse = Depends(validate_user_from_token)
) -> UserResponse:
    """Ensure the authenticated user account is active."""
    if not authenticated_user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return authenticated_user