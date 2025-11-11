# app/models/user.py
from datetime import datetime, timedelta
import uuid
from typing import Optional, Dict, Any

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import ValidationError

from app.schemas.base import UserCreate
from app.schemas.user import UserResponse, Token

Base = declarative_base()

# Password hashing configuration
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration - should be moved to config file
JWT_SECRET = "your-secret-key"
JWT_ALGO = "HS256"
TOKEN_VALIDITY_MINS = 30

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User(name={self.first_name} {self.last_name}, email={self.email})>"

    @staticmethod
    def hash_password(plain_pwd: str) -> str:
        """Generate bcrypt hash from plain password."""
        return password_hasher.hash(plain_pwd)

    def verify_password(self, input_password: str) -> bool:
        """Check if input password matches stored hash."""
        return password_hasher.verify(input_password, self.password)

    @staticmethod
    def create_access_token(payload: dict, validity_period: Optional[timedelta] = None) -> str:
        """Generate JWT access token with expiration."""
        encoded_data = payload.copy()
        expiry_time = datetime.utcnow() + (validity_period or timedelta(minutes=TOKEN_VALIDITY_MINS))
        encoded_data.update({"exp": expiry_time})
        return jwt.encode(encoded_data, JWT_SECRET, algorithm=JWT_ALGO)

    @staticmethod
    def verify_token(jwt_token: str) -> Optional[UUID]:
        """Decode and validate JWT token, return user ID."""
        try:
            decoded_payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGO])
            uid = decoded_payload.get("sub")
            return uuid.UUID(uid) if uid else None
        except (JWTError, ValueError):
            return None

    @classmethod
    def register(cls, db, registration_data: Dict[str, Any]) -> "User":
        """Create new user account with validation checks."""
        try:
            # Validate password length requirement
            pwd = registration_data.get('password', '')
            if len(pwd) < 6:  # Must be at least 6 characters
                raise ValueError("Password must be at least 6 characters long")
            
            # Check for existing email or username
            duplicate_check = db.query(cls).filter(
                (cls.email == registration_data.get('email')) |
                (cls.username == registration_data.get('username'))
            ).first()
            
            if duplicate_check:
                raise ValueError("Username or email already exists")

            # Validate input data with Pydantic schema
            validated_data = UserCreate.model_validate(registration_data)
            
            # Create user instance
            user_instance = cls(
                first_name=validated_data.first_name,
                last_name=validated_data.last_name,
                email=validated_data.email,
                username=validated_data.username,
                password=cls.hash_password(validated_data.password),
                is_active=True,
                is_verified=False
            )
            
            db.add(user_instance)
            db.flush()
            return user_instance
            
        except ValidationError as validation_err:
            raise ValueError(str(validation_err)) # pragma: no cover
        except ValueError as val_err:
            raise val_err

    @classmethod
    def authenticate(cls, db, login_identifier: str, login_password: str) -> Optional[Dict[str, Any]]:
        """Verify credentials and return authentication token with user info."""
        user_record = db.query(cls).filter(
            (cls.username == login_identifier) | (cls.email == login_identifier)
        ).first()

        if not user_record or not user_record.verify_password(login_password):
            return None # pragma: no cover

        user_record.last_login = datetime.utcnow()
        db.commit()

        # Generate response with token and user data
        user_details = UserResponse.model_validate(user_record)
        auth_response = Token(
            access_token=cls.create_access_token({"sub": str(user_record.id)}),
            token_type="bearer",
            user=user_details
        )

        return auth_response.model_dump()