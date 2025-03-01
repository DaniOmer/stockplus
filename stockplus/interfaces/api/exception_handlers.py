"""
Exception handlers for the API.
This module contains the exception handlers for the API.
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from stockplus.domain.exceptions import (
    DomainException,
    UserAlreadyExistsException,
    ResourceNotFoundException,
    InvalidCredentialsException,
    ValidationException
)

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for the API.
    
    This function handles exceptions raised by the API views and returns
    appropriate responses.
    
    Args:
        exc: The exception that was raised
        context: The context in which the exception was raised
        
    Returns:
        Response: A response object with the appropriate status code and error message
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # If the exception is already handled by DRF, return the response
    if response is not None:
        return response

    # Handle domain exceptions
    if isinstance(exc, UserAlreadyExistsException):
        logger.warning(f"User already exists: {str(exc)}")
        return Response(
            {'detail': str(exc)},
            status=status.HTTP_409_CONFLICT
        )
    elif isinstance(exc, ResourceNotFoundException):
        logger.warning(f"Resource not found: {str(exc)}")
        return Response(
            {'detail': str(exc)},
            status=status.HTTP_404_NOT_FOUND
        )
    elif isinstance(exc, InvalidCredentialsException):
        logger.warning(f"Invalid credentials: {str(exc)}")
        return Response(
            {'detail': str(exc)},
            status=status.HTTP_401_UNAUTHORIZED
        )
    elif isinstance(exc, ValidationException):
        logger.warning(f"Validation error: {str(exc)}")
        return Response(
            {'detail': str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )
    elif isinstance(exc, DomainException):
        logger.warning(f"Domain exception: {str(exc)}")
        return Response(
            {'detail': str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Handle unexpected exceptions
    logger.error(f"Unexpected exception: {str(exc)}", exc_info=True)
    return Response(
        {'detail': 'An unexpected error occurred.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
