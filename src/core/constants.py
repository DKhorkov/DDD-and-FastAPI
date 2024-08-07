class ErrorDetails:
    """
    Base error messages for custom exceptions.
    """

    SERVER_ERROR: str = 'Server error'
    PERMISSION_DENIED: str = 'Permission denied'
    BAD_REQUEST: str = 'Bad Request'
    MESSAGEBUS_MESSAGE_ERROR: str = 'Message bus message should be eiter of Event type, or Command type'
