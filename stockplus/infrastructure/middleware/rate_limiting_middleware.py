"""
Rate limiting middleware for the stockplus project.
This module contains the rate limiting middleware for the stockplus project.
"""

import time
from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import Throttled

class RateLimitingMiddleware:
    """
    Rate limiting middleware for the stockplus project.
    
    This middleware limits the number of requests a user can make to certain endpoints
    within a specified time period.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Endpoints to rate limit (path, requests, period in seconds)
        self.rate_limited_endpoints = [
            # Avatar endpoints - 5 requests per minute
            ('/api/avatar/upload/', 5, 60),
            ('/api/avatar/remove/', 5, 60),
            ('/api/avatar/url/', 5, 60),
        ]
    
    def __call__(self, request):
        # Check if the request path is rate limited
        for path, max_requests, period in self.rate_limited_endpoints:
            if request.path.startswith(path):
                # Get the user ID or IP address if not authenticated
                if request.user.is_authenticated:
                    key = f"rate_limit:{request.user.id}:{path}"
                else:
                    key = f"rate_limit:{request.META.get('REMOTE_ADDR')}:{path}"
                
                # Get the current count and timestamp
                rate_limit_data = cache.get(key)
                current_time = int(time.time())
                
                if rate_limit_data is None:
                    # First request, set count to 1
                    cache.set(key, {'count': 1, 'timestamp': current_time}, period)
                else:
                    # Check if the period has expired
                    if current_time - rate_limit_data['timestamp'] > period:
                        # Reset the count
                        cache.set(key, {'count': 1, 'timestamp': current_time}, period)
                    else:
                        # Increment the count
                        if rate_limit_data['count'] >= max_requests:
                            # Rate limit exceeded
                            retry_after = period - (current_time - rate_limit_data['timestamp'])
                            raise Throttled(detail={
                                'message': f'Rate limit exceeded. Try again in {retry_after} seconds.',
                                'retry_after': retry_after
                            }, code='throttled')
                        else:
                            # Update the count
                            rate_limit_data['count'] += 1
                            cache.set(key, rate_limit_data, period)
                
                break
        
        # Continue processing the request
        return self.get_response(request)
