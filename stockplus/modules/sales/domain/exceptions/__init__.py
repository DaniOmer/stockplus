class SaleNotFoundError(Exception):
    """
    Exception raised when a sale is not found.
    """
    def __init__(self, sale_id: int):
        self.sale_id = sale_id
        super().__init__(f"Sale with ID {sale_id} not found.")


class SaleItemNotFoundError(Exception):
    """
    Exception raised when a sale item is not found.
    """
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Sale item with ID {item_id} not found.")


class InvoiceNotFoundError(Exception):
    """
    Exception raised when an invoice is not found.
    """
    def __init__(self, invoice_id: int):
        self.invoice_id = invoice_id
        super().__init__(f"Invoice with ID {invoice_id} not found.")


class DuplicateSaleError(Exception):
    """
    Exception raised when a duplicate sale is detected.
    """
    def __init__(self, invoice_number: str):
        self.invoice_number = invoice_number
        super().__init__(f"Sale with invoice number {invoice_number} already exists.")


class InsufficientStockError(Exception):
    """
    Exception raised when there is insufficient stock for a product.
    """
    def __init__(self, product_id: int, requested: int, available: int):
        self.product_id = product_id
        self.requested = requested
        self.available = available
        super().__init__(
            f"Insufficient stock for product with ID {product_id}. "
            f"Requested: {requested}, Available: {available}."
        )


class SaleAlreadyCancelledError(Exception):
    """
    Exception raised when attempting to cancel a sale that is already cancelled.
    """
    def __init__(self, sale_id: int):
        self.sale_id = sale_id
        super().__init__(f"Sale with ID {sale_id} is already cancelled.")
