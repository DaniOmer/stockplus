from rest_framework.views import exception_handler
from rest_framework.response import Response
from stockplus.domain.exceptions import DomainException

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, DomainException):
        errors = []
        
        if isinstance(exc.errors, dict):
            # Gestion des erreurs de type DRF (dictionnaire)
            for field, error_details in exc.errors.items():
                for error_detail in error_details:
                    errors.append({
                        "field": field,
                        "message": str(error_detail)
                    })
        elif isinstance(exc.errors, list):
            # Gestion des erreurs de type Pydantic (liste de dictionnaires)
            for error in exc.errors:
                error_info = {}
                if isinstance(error, dict):
                    # Extraction pour les erreurs Pydantic avec 'loc' et 'msg'
                    if 'loc' in error:
                        loc = error['loc']
                        if isinstance(loc, (list, tuple)) and len(loc) > 0:
                            error_info["field"] = loc[0]
                        else:
                            error_info["field"] = 'non_field_errors'
                        error_info["message"] = error.get('msg', '')
                    else:
                        # Fallback pour d'autres structures de dictionnaire
                        error_info["field"] = error.get('field', 'non_field_errors')
                        error_info["message"] = error.get('message', str(error))
                else:
                    # Gestion des erreurs simples (string)
                    error_info["field"] = 'non_field_errors'
                    error_info["message"] = str(error)
                errors.append(error_info)
        else:
            # Cas où exc.errors n'est ni un dict ni une liste
            errors.append({
                "field": 'non_field_errors',
                "message": str(exc.errors)
            })

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