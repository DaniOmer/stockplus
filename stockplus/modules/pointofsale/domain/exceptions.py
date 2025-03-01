class PointOfSaleError(Exception):
    """Base exception for all point of sale related errors."""
    pass


class PointOfSaleNotFoundError(PointOfSaleError):
    """Raised when a point of sale is not found."""
    def __init__(self, point_of_sale_id: int = None, message: str = None):
        self.point_of_sale_id = point_of_sale_id
        self.message = message or f"Point of sale with id {point_of_sale_id} not found."
        super().__init__(self.message)


class CollaboratorNotFoundError(PointOfSaleError):
    """Raised when a collaborator is not found."""
    def __init__(self, email: str = None, message: str = None):
        self.email = email
        self.message = message or f"Collaborator with email {email} not found."
        super().__init__(self.message)


class CompanyNotFoundError(PointOfSaleError):
    """Raised when a company is not found."""
    def __init__(self, company_id: int = None, message: str = None):
        self.company_id = company_id
        self.message = message or f"Company with id {company_id} not found."
        super().__init__(self.message)
