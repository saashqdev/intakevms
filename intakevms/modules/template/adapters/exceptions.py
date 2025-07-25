"""Adapter-layer exceptions for the template module.

This module defines exceptions related to template operations at the adapter
level.

Classes:
    - TemplateNotFoundException: Exception raised when a template is not found
        in the database.
"""

from intakevms.abstracts.base_exception import BaseCustomException


class TemplateNotFoundInDBException(BaseCustomException):
    """Exception raised when a template is not found in the database."""