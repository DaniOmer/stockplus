class ProductError(Exception):
    """Base exception for all product related errors."""
    pass


class ProductNotFoundError(ProductError):
    """Raised when a product is not found."""
    def __init__(self, product_id: int = None, message: str = None):
        self.product_id = product_id
        self.message = message or f"Product with id {product_id} not found."
        super().__init__(self.message)


class BrandNotFoundError(ProductError):
    """Raised when a brand is not found."""
    def __init__(self, brand_id: int = None, message: str = None):
        self.brand_id = brand_id
        self.message = message or f"Brand with id {brand_id} not found."
        super().__init__(self.message)


class ProductCategoryNotFoundError(ProductError):
    """Raised when a product category is not found."""
    def __init__(self, category_id: int = None, message: str = None):
        self.category_id = category_id
        self.message = message or f"Product category with id {category_id} not found."
        super().__init__(self.message)


class ProductFeatureNotFoundError(ProductError):
    """Raised when a product feature is not found."""
    def __init__(self, feature_id: int = None, message: str = None):
        self.feature_id = feature_id
        self.message = message or f"Product feature with id {feature_id} not found."
        super().__init__(self.message)


class ProductVariantNotFoundError(ProductError):
    """Raised when a product variant is not found."""
    def __init__(self, variant_id: int = None, message: str = None):
        self.variant_id = variant_id
        self.message = message or f"Product variant with id {variant_id} not found."
        super().__init__(self.message)


class PointOfSaleProductVariantNotFoundError(ProductError):
    """Raised when a point of sale product variant is not found."""
    def __init__(self, pos_variant_id: int = None, message: str = None):
        self.pos_variant_id = pos_variant_id
        self.message = message or f"Point of sale product variant with id {pos_variant_id} not found."
        super().__init__(self.message)


class CompanyNotFoundError(ProductError):
    """Raised when a company is not found."""
    def __init__(self, company_id: int = None, message: str = None):
        self.company_id = company_id
        self.message = message or f"Company with id {company_id} not found."
        super().__init__(self.message)


class DuplicateProductError(ProductError):
    """Raised when trying to create a product with a name that already exists."""
    def __init__(self, name: str = None, message: str = None):
        self.name = name
        self.message = message or f"Product with name '{name}' already exists."
        super().__init__(self.message)


class DuplicateBrandError(ProductError):
    """Raised when trying to create a brand with a name that already exists."""
    def __init__(self, name: str = None, message: str = None):
        self.name = name
        self.message = message or f"Brand with name '{name}' already exists."
        super().__init__(self.message)


class DuplicateProductCategoryError(ProductError):
    """Raised when trying to create a product category with a name that already exists."""
    def __init__(self, name: str = None, message: str = None):
        self.name = name
        self.message = message or f"Product category with name '{name}' already exists."
        super().__init__(self.message)
