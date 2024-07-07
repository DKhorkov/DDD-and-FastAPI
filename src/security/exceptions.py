from src.security.constants import ErrorDetails
from src.core.exceptions import PreconditionFailedError


class InvalidTokenError(PreconditionFailedError):
    DETAIL = ErrorDetails.INVALID_TOKEN
