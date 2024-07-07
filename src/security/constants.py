from src.core.constants import ErrorDetails as BaseErrorDetails


class ErrorDetails(BaseErrorDetails):
    """
    Security error messages for custom exceptions.
    """

    INVALID_TOKEN: str = 'Token has expired or is invalid'
