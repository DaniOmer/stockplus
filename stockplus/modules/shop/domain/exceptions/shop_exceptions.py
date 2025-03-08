class ShopError(Exception):
    """Base exception for shop errors."""
    pass


class CustomerNotFoundError(ShopError):
    """Exception raised when a customer is not found."""
    def __init__(self, customer_id):
        self.customer_id = customer_id
        super().__init__(f"Customer with ID {customer_id} not found.")


class ProductNotFoundError(ShopError):
    """Exception raised when a product is not found."""
    def __init__(self, product_id):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found.")


class PriceNotFoundError(ShopError):
    """Exception raised when a price is not found."""
    def __init__(self, price_id):
        self.price_id = price_id
        super().__init__(f"Price with ID {price_id} not found.")


class CustomerAlreadyExistsError(ShopError):
    """Exception raised when a customer already exists."""
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"Customer for user with ID {user_id} already exists.")


class ProductAlreadyExistsError(ShopError):
    """Exception raised when a product already exists."""
    def __init__(self, name):
        self.name = name
        super().__init__(f"Product with name '{name}' already exists.")


class StripeError(ShopError):
    """Exception raised when there is an error with Stripe."""
    def __init__(self, message):
        super().__init__(f"Stripe error: {message}")
