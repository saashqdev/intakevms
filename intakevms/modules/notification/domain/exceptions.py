"""Custom exceptions for notification domain.

This module defines custom exceptions that are used within the notification
domain, particularly for email notifications.
"""

from typing import Any

from intakevms.abstracts.base_exception import BaseCustomException


class NoRecipientsSpecifiedForEmailNotification(BaseCustomException):
    """Raised when recipients are not specified for email notification."""

    def __init__(self, message: str, *args: Any) -> None:  # noqa: ANN401 # TODO need to parameterize the arguments correctly, in accordance with static typing
        """Initialize the `NoRecipientsSpecifiedForEmailNotification`."""
        super().__init__(message, *args)


class NotificationSMTPException(BaseCustomException):
    """Raised when getting error while using smtp."""

    def __init__(self, message: str, *args: Any) -> None:  # noqa: ANN401 # TODO need to parameterize the arguments correctly, in accordance with static typing
        """Initialize the NotificationSMTPException."""
        super().__init__(message, *args)
