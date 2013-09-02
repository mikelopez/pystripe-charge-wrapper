"""
Stripe - Python Payments wrapper
License: MIT
dev@scidentify.info
git@github.com/mikelopez/stripe-payments-wrapper.git

Simple class to create captured and uncaptured charges, 
retrieve and capture them.

"""

import stripe
from decimal import Decimal

class PyStripeCharges(object):
    """
    A convenient basic class to help utilize some of 
    stripes payments. Mainly focused on Stripes Charge() feature, 
    and lightly touching the Customer() feature. 

    Creates & Refunds captured/uncaptured charges, retreives charges, 
    and handles charging the uncaptured charges.

    """
    stripe_api_key = None
    price = Decimal('0.00')
    stripe_customer = None
    stripe_charge = None

    # the current stripe charge object
    stripe_object = None

    def __init__(self, stripe_api_key=None):
        if stripe_api_key:
            self.set_api_key(stripe_api_key)

        if not self.get_api_key():
            raise Exception("No Stripe API Key")

    def get_price(self):
        """Gets the price that is currently set on self."""
        return getattr(self, 'price')

    def get_api_key(self):
        """Gets the stripe api key set on self."""
        return getattr(self, 'stripe_api_key')

    def set_api_key(self, value):
        """Set the API keys needed to the class."""
        setattr(self, 'stripe_api_key', value)

    def set_price(self, value):
        """Sets the price to charge a customer."""
        try:
            setattr(self, 'price', Decimal(value))
        except InvalidOperation:
            raise Exception("Invalid numeric price %s" % value)

    def to_cents(self):
        """ Convert the price down to cents """
        if self.get_price() == 0:
            return 0
            # over a dollah
        return int(Decimal(self.get_price() * 100))

    def create_captured_charge(self, card):
        """ Create a captured charge with card
        Card should be a dictionary with the following keys:
         - exp_month = cards expire month
         - exp_year = cards expire year
         - cvc = the card cvc on the back
         - number = the card number
        """
        if self.get_price() > 0:
            amount = self.to_cents()
            try:
                stripe.api_key = self.get_api_key()
                if not self.stripe_customer:
                    self.stripe_customer = stripe.Customer.create(
                        description='Temporal customer',
                        card=card
                    )
                self.stripe_object = stripe.Charge.create(
                    currency="usd",
                    amount=amount,
                    capture='true',
                    customer=self.stripe_customer.id
                )
            except stripe.CardError, e:
                raise Exception("Charge Card Error: %s" % e)
            except Exception, e:
                raise Exception("Charge Exception: %s" % e)
            self.stripe_id = self.stripe_object.__dict__.get('id')
            stripe.api_key = None

    def create_uncaptured_charge(self, card):
        """ Create a captured charge with card
        Card should be a dictionary with the following keys:
         - exp_month = cards expire month
         - exp_year = cards expire year
         - cvc = the card cvc on the back
         - number = the card number
        """
        if self.get_price() > 0:
            amount = self.to_cents()
            try:
                stripe.api_key = self.get_api_key()
                if not self.stripe_customer:
                    self.stripe_customer = stripe.Customer.create(
                        description='Temporal customer',
                        card=card
                    )
                self.stripe_object = stripe.Charge.create(
                    currency="usd",
                    amount=amount,
                    capture='false',
                    customer=self.stripe_customer.id
                )
            except stripe.CardError, e:
                raise Exception("Charge Card Error: %s" % e)
            except Exception, e:
                raise Exception("Charge Exception: %s" % e)
            self.stripe_id = self.stripe_object.__dict__.get('id')
            stripe.api_key = None

    def refund_charge(self):
        """ Refunds a charge """
        stripe.api_key = self.get_api_key()
        try:
            self.stripe_object = stripe.Charge.retrieve(id=self.stripe_id)
        except Exception, e:
            raise Exception("Error Retrieving Charge %s" % e)
        try:
            self.stripe_object.refund()
        except Exception, e:
            raise Exception("Refund Exception %s" % e)
        stripe.api_key = None

    def capture_charge(self, **kwargs):
        """ Captures a charge.
        Pass expand=['object'] to expand the charge data retrieval beyond
        the basic payment information.
        """
        stripe.api_key = self.get_api_key()
        if expand:
            kwargs = {'expand': ['customer']}
        try:
            self.stripe_object = stripe.Charge.retrieve(id=self.stripe_id, **kwargs)
        except Exception, e:
            raise Exception("Error Retrieving Charge %s" % e)
        try:
            self.stripe_object.capture()
        except Exception, e:
            raise Exception("Capture Exception  %s" % e)
        stripe.api_key = None

    def delete_customer(self):
        """ Deletes the customer. """
        if self.stripe_customer:
            try:
                self.stripe_customer.delete()
                self.stripe_customer = None
            except Exception, e:
                raise Exception("Customer Exception  %s" % e)

