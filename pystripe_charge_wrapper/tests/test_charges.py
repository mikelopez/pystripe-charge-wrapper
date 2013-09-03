import sys
from unittest import TestCase, TestSuite, TextTestRunner
from decimal import Decimal
from termprint import *
sys.path.append('../')
from pystripe_charges import *

try:
    import test_settings as settings
    STRIPE_API_KEY = getattr(settings, "TEST_STRIPE_SECRET")
except ImportError:
    STRIPE_API_KEY = "tGN0bIwXnHdwOa85VABjPdSn8nWY7G7I"

card_scenarios = {'card_declined': '4000000000000002',
                  'incorrect_number': '42424242424241'}

# debug types
i, e, w = "INFO", "ERROR", "WARNING"

class TestStripeCharges(TestCase):
    """Test the stripe charge functionality."""

    stripe_api_key = STRIPE_API_KEY
    card = {'exp_month': '1', 'exp_year': '2016',
            'cvc': '222', 'number': '4242424242424242'}

    def setUp(self):
        if not self.stripe_api_key:
            raise Exception("No valid api key found.")
            sys.exit(1)


    def __init_stripe(self):
        """ Return a stripe init. """
        return StripeCharges(stripe_api_key=getattr(self, "stripe_api_key"))


    def test_charge(self):
        """Test the charges."""
        termprint(i, "Testing Charge...")
        cl = StripeCharges(stripe_api_key=getattr(self, "stripe_api_key"))
        self.assertEquals(getattr(cl, "stripe_api_key"), 
                          getattr(self, "stripe_api_key"))
        cl.set_price('1.00')
        self.assertEquals(cl.get_price(), Decimal('1.00'))
        charge_id = cl.create_charge(self.card)
        response = cl.capture_charge()
        termprint(e, "Charge ID %s" % charge_id)
        termprint(e, "Charge Capture %s" % response)


    def test_to_cents(self):
        """Test the conversion of the price to cents."""
        termpritn(i, "Test conversion of amount$ to pennies.")
        cl = StripeCharges(stripe_api_key=getattr(self, "stripe_api_key"))
        cl.set_price('1.00')
        self.assertEquals(self.to_cents(), 100)
        self.assertEquals(self.to_cents(),
                          int(Decimal(self.get_price() * 100)))
        

    def test_create_captured_charge(self):
        """ Test creating a test charge. """
        termprint(i, "Test create captured charge...")
        cl = StripeCharges(stripe_api_key=getattr(self, "stripe_api_key"))
        cl.set_price('1.00')
        charge_id = cl.create_charge(self.card, capture=True)
        self.assertEquals(charge_id, cl.stripe_id)
        termprint(e, charge_id)
        termprint(e, cl.stripe_id)
        # test charge retrieval!
        self.assertTrue(cl.retrieve_charge(id=charge_id))
        self.assertEquals(cl.stripe_object.get('captured'), True)


    def test_create_uncaptured_charge(self):
        """ Create an uncaptured charge by passing kwarg."""
        termprint(i, "Test create uncaptured charge.")
        cl = StripeCharges(stripe_api_key=getattr(self, "stripe_api_key"))
        cl.set_price('1.00')
        charge_id = cl.create_charge(self.card, capture=False)
        self.assertEquals(charge_id, cl.stripe_id)
        # test charge retrieval!
        self.assertTrue(cl.retrieve_charge(id=charge_id))
        self.assertTrue(charge_id)
        # charge is not captured!
        self.assertEquals(cl.stripe_object.get('captured'), False)
        cl.capture_charge()
        self.assertEquals(cl.stripe_object.get('captured'), True)


    def test_refund(self):
        """ Test refunding an order """
        termprint(i, "Test create refund.")
        cl = StripeCharges(stripe_api_key=getattr(self, "stripe_api_key"))
        cl.set_price('1.00')
        charge_id = cl.create_charge(self.card, capture=True)
        charge = cl.retrieve_charge(id=charge_id)
        self.assertTrue(charge)
        # refunds the most recent
        result = self.assertTrue(cl.refund_charge())
        termprint(w, result)
        # both charges should be the same, since charge_id
        # is the charge that is in self.stripe_object
        self.assertEquals(cl.stripe_object.get('refunded'), True)


    def test_retrieve_charges(self):
        """Test retrieving the charge."""
        termprint(i, "Test retrieve charges...")
        cl = StripeCharges(stripe_api_key=getattr(self, "stripe_api_key"))
        cl.set_price('1.00')
        charge_id = cl.create_charge(self.card, capture=False)
        try:
            charge = cl.retrieve_charge(id='ass')
            assert False, "Nah uh, need a valid integer."
        except ValueError:
            assert True
        # shoudl get the latest charge.
        charge1 = cl.retrieve_charge() 
        charge2 = cl.retrieve_charge(id=self.id)
        # now test with a different order
        new_charge = cl.create_charge(self.card, captured=False)



