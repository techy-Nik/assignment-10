import pytest
from pydantic import ValidationError
from app.schemas.base import BaseUserSchema, SecurePasswordValidator, UserCreate, UserLogin


def test_base_user_schema_valid():
    """Test BaseUserSchema with valid data."""
    input_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@email.com",
        "username": "alicesmith",
    }
    user_obj = BaseUserSchema(**input_data)
    assert user_obj.first_name == "Alice"
    assert user_obj.email == "alice.smith@email.com"


def test_base_user_schema_invalid_email():
    """Test BaseUserSchema with invalid email."""
    input_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "not-valid-email",
        "username": "alicesmith",
    }
    with pytest.raises(ValidationError):
        BaseUserSchema(**input_data)


def test_secure_password_validator_valid():
    """Test SecurePasswordValidator with valid password."""
    input_data = {"password": "MyPass456"}
    pwd_validator = SecurePasswordValidator(**input_data)
    assert pwd_validator.password == "MyPass456"


def test_secure_password_validator_invalid_short():
    """Test SecurePasswordValidator with short password."""
    input_data = {"password": "short"}
    with pytest.raises(ValidationError):
        SecurePasswordValidator(**input_data)


def test_secure_password_validator_missing_uppercase():
    """Test SecurePasswordValidator with no uppercase letter."""
    input_data = {"password": "lowercase1"}
    with pytest.raises(ValidationError, match="Password must contain at least one uppercase letter"):
        SecurePasswordValidator(**input_data)


def test_secure_password_validator_missing_lowercase():
    """Test SecurePasswordValidator with no lowercase letter."""
    input_data = {"password": "UPPERCASE1"}
    with pytest.raises(ValidationError, match="Password must contain at least one lowercase letter"):
        SecurePasswordValidator(**input_data)


def test_secure_password_validator_missing_digit():
    """Test SecurePasswordValidator with no digit."""
    input_data = {"password": "NoDigitsHere"}
    with pytest.raises(ValidationError, match="Password must contain at least one digit"):
        SecurePasswordValidator(**input_data)


def test_user_create_valid():
    """Test UserCreate with valid data."""
    input_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@email.com",
        "username": "alicesmith",
        "password": "MyPass456",
    }
    created_user = UserCreate(**input_data)
    assert created_user.username == "alicesmith"
    assert created_user.password == "MyPass456"


def test_user_create_invalid_password():
    """Test UserCreate with invalid password."""
    input_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@email.com",
        "username": "alicesmith",
        "password": "short",
    }
    with pytest.raises(ValidationError):
        UserCreate(**input_data)


def test_user_login_valid():
    """Test UserLogin with valid data."""
    input_data = {"username": "alicesmith", "password": "MyPass456"}
    login_obj = UserLogin(**input_data)
    assert login_obj.username == "alicesmith"


def test_user_login_invalid_username():
    """Test UserLogin with short username."""
    input_data = {"username": "as", "password": "MyPass456"}
    with pytest.raises(ValidationError):
        UserLogin(**input_data)


def test_user_login_invalid_password():
    """Test UserLogin with invalid password."""
    input_data = {"username": "alicesmith", "password": "short"}
    with pytest.raises(ValidationError):
        UserLogin(**input_data)