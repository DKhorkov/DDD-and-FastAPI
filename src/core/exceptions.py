from typing import Any
from fastapi import HTTPException, status

from src.core.constants import ErrorDetails


class DetailedHTTPException(HTTPException):
    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str = ErrorDetails.SERVER_ERROR

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class PermissionDeniedError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = ErrorDetails.PERMISSION_DENIED


class NotFoundError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class AlreadyExistsError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT


class BadRequestError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = ErrorDetails.BAD_REQUEST


class PreconditionFailedError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_412_PRECONDITION_FAILED


class ValidationError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
