from builder.applications.shop import utils

class CustomerService:
    @staticmethod
    def create_stripe_customer(name='', email='', address='', metadata={}, raw=False):
        """Create a new stripe customer"""
        stripe = utils.init_stripe()
        response = stripe.Customer.create(
            name=name,
            email=email,
            address=address,
            metadata=metadata
        )
        if raw:
            return response
        return response.id