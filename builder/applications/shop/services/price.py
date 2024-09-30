from builder.utils import init_stripe

class PriceService:
    @staticmethod
    def create_stripe_price( 
        currency='usd', 
        unit_amount=1000, 
        interval="month", 
        interval_count=1, 
        product=None, 
        metadata={},
        raw=False
    ):
        if product is not None:
            stripe = init_stripe()
            response = stripe.Price.create(
                currency=currency,
                unit_amount=unit_amount,
                recurring={
                    "interval": interval,
                    "interval_count": interval_count
                },
                product=product,
                metadata=metadata
            )
            if raw:
                return response
            return response.id
        return None