# tests/integration/test_dependencies.py

import pytest
from unittest.mock import MagicMock, patch, ANY
from fastapi import HTTPException
from app.auth.dependencies import validate_user_from_token, ensure_user_is_active
from app.schemas.user import UserResponse
from app.models.user import User
from uuid import uuid4
from datetime import datetime

# Test data for active user
active_test_user = User(
    id=uuid4(),
    username="testuser",
    email="test@example.com",
    first_name="Test",
    last_name="User",
    is_active=True,
    is_verified=True,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

# Test data for inactive user
disabled_test_user = User(
    id=uuid4(),
    username="inactiveuser",
    email="inactive@example.com",
    first_name="Inactive",
    last_name="User",
    is_active=False,
    is_verified=False,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

# Mock database session fixture
@pytest.fixture
def db_mock():
    return MagicMock()

# Mock token verification fixture
@pytest.fixture
def token_verification_mock():
    with patch.object(User, 'verify_token') as mock:
        yield mock

# Test validate_user_from_token with valid credentials
def test_validate_user_from_token_success(db_mock, token_verification_mock):
    token_verification_mock.return_value = active_test_user.id
    db_mock.query.return_value.filter.return_value.first.return_value = active_test_user

    result = validate_user_from_token(db=db_mock, auth_token="validtoken")

    assert isinstance(result, UserResponse)
    assert result.id == active_test_user.id
    assert result.username == active_test_user.username
    assert result.email == active_test_user.email
    assert result.first_name == active_test_user.first_name
    assert result.last_name == active_test_user.last_name
    assert result.is_active == active_test_user.is_active
    assert result.is_verified == active_test_user.is_verified
    assert result.created_at == active_test_user.created_at
    assert result.updated_at == active_test_user.updated_at

    token_verification_mock.assert_called_once_with("validtoken")
    db_mock.query.assert_called_once_with(User)
    db_mock.query.return_value.filter.assert_called_once_with(ANY)
    db_mock.query.return_value.filter.return_value.first.assert_called_once()

# Test validate_user_from_token with invalid token
def test_validate_user_from_token_bad_token(db_mock, token_verification_mock):
    token_verification_mock.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        validate_user_from_token(db=db_mock, auth_token="invalidtoken")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"

    token_verification_mock.assert_called_once_with("invalidtoken")
    db_mock.query.assert_not_called()

# Test validate_user_from_token when user not found in database
def test_validate_user_from_token_user_not_found(db_mock, token_verification_mock):
    token_verification_mock.return_value = active_test_user.id
    db_mock.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        validate_user_from_token(db=db_mock, auth_token="validtoken")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"

    token_verification_mock.assert_called_once_with("validtoken")
    db_mock.query.assert_called_once_with(User)
    db_mock.query.return_value.filter.assert_called_once_with(ANY)
    db_mock.query.return_value.filter.return_value.first.assert_called_once()

# Test ensure_user_is_active with active user
def test_ensure_user_is_active_success(db_mock, token_verification_mock):
    token_verification_mock.return_value = active_test_user.id
    db_mock.query.return_value.filter.return_value.first.return_value = active_test_user

    authenticated_user = validate_user_from_token(db=db_mock, auth_token="validtoken")
    result = ensure_user_is_active(authenticated_user=authenticated_user)

    assert isinstance(result, UserResponse)
    assert result.is_active is True

# Test ensure_user_is_active with inactive user
def test_ensure_user_is_active_failure(db_mock, token_verification_mock):
    token_verification_mock.return_value = disabled_test_user.id
    db_mock.query.return_value.filter.return_value.first.return_value = disabled_test_user

    authenticated_user = validate_user_from_token(db=db_mock, auth_token="validtoken")

    with pytest.raises(HTTPException) as exc_info:
        ensure_user_is_active(authenticated_user=authenticated_user)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Inactive user"