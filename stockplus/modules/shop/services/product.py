from stockplus.utils import init_stripe

class ProductService:
    @staticmethod
    def create_stripe_product(name='', description='', active=False, metadata={}, raw=False):
        stripe = init_stripe()
        response = stripe.Product.create(
            name=name, 
            description=description, 
            active=active, 
            metadata=metadata
        )

        if raw:
            return response
        return response.id