class DomainException(Exception):
    """Base exception with configurable error type"""
    status_code = 400
    error_type = 'domain_error'
    errors = []
    
    def __init__(self, message=None, **kwargs):
        self.message = message or self.default_message
        self.errors = kwargs.get('errors', self.errors)
        super().__init__(self.message)