"""
Authentication logging middleware.
This middleware logs authentication-related information for all requests.
"""

import logging

logger = logging.getLogger(__name__)

class AuthLoggingMiddleware:
    """
    Middleware to log authentication-related information for all requests.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Skip logging for static files and admin requests
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return self.get_response(request)
        
        # Log authentication details
        logger.info(f"=== Authentication Request: {request.path} ===")
        logger.info(f"Method: {request.method}")
        
        # Log authentication headers
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header:
            # Mask the token value for security
            parts = auth_header.split(' ', 1)
            if len(parts) == 2:
                token_type, token = parts
                masked_token = token[:10] + '...' if len(token) > 10 else token
                logger.info(f"Authorization: {token_type} {masked_token}")
            else:
                logger.info(f"Authorization header malformed: {auth_header}")
        else:
            logger.info("No Authorization header present")
        
        # Log user information
        if hasattr(request, 'user'):
            logger.info(f"User authenticated: {request.user.is_authenticated}")
            if request.user.is_authenticated:
                logger.info(f"User ID: {request.user.id}")
                logger.info(f"User email: {request.user.email}")
            else:
                logger.info("User is not authenticated")
        
        # Process the request
        response = self.get_response(request)
        
        # Log response status
        logger.info(f"Response status: {response.status_code}")
        
        return response
