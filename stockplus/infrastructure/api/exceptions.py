from rest_framework.views import exception_handler
from rest_framework.response import Response

from stockplus.domain.exceptions import DomainException

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, DomainException):

        errors = []
        for e in exc.errors:
            error = {}
            error["field"] = e.get("loc")[0]
            error["message"] = e.get("msg")
            errors.append(error)

        return Response(
            {
                'message': str(exc),
                'error_type': exc.error_type,
                'errors': errors,
                'data': {}
            },
            status=exc.status_code
        )
        
    return response