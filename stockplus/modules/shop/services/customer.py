from stockplus.utils import init_stripe

class CustomerService:
    @staticmethod
    def create_stripe_customer(name='', email='', address='', metadata={}, raw=False):
        """Create a new stripe customer"""
        stripe = init_stripe()
        response = stripe.Customer.create(
            name=name,
            email=email,
            address=address,
            metadata=metadata
        )
        if raw:
            return response
        return response.id