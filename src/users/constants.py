from src.core.constants import ErrorDetails as BaseErrorDetails
from src.users.config import UserValidationConfig


class ErrorDetails(BaseErrorDetails):
    """
    Authorization and authentication error messages for custom exceptions.
    """

    USER_NOT_AUTHENTICATED: str = 'User not authenticated'
    PASSWORD_VALIDATION_ERROR: str = (f'Password must be between {UserValidationConfig.PASSWORD_MIN_LENGTH} and '
                                      f'{UserValidationConfig.PASSWORD_MAX_LENGTH} characters inclusive')
    USERNAME_VALIDATION_ERROR: str = (f'Username must be between {UserValidationConfig.USERNAME_MIN_LENGTH} and '
                                      f'{UserValidationConfig.USERNAME_MAX_LENGTH} characters inclusive')
    INVALID_PASSWORD: str = 'Provided password is invalid'
    INVALID_USER: str = 'Current user is invalid'
    USER_ALREADY_EXISTS: str = 'User with provided credentials already exists'
    USER_NOT_FOUND: str = 'User with provided credentials not found'
    USER_ATTRIBUTE_REQUIRED: str = 'user id, email or username is required'
