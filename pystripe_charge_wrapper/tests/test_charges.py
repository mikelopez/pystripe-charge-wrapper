from unittest import TestCase, TestSuite, TestTextRunner
from decimal import Decimal

try:
    import test_settings
except ImportError:
    raise Exception("No test_settings found. Need API Keys")
    sys.exit(1)

card_scenarios = {'card_declined': '4000000000000002',
                  'incorrect_number': '42424242424241'}


class TestStripeCharges(TestCase):
    """Test the stripe charge functionality."""

    stripe_api_key = getattr(settings, "TEST_STRIPE_SECRET")
    card = {'currency': "USD", 'amount': cl.get_price(), 
            'exp_month': '1', 'exp_year': '2016', 
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
        cl = self.__init_stripe()
        self.assertEquals(getattr(cl, "stripe_api_key"), getattr(self, "stripe_api_key"))

        cl.set_price('1.00')
        self.assertEquals(cl.get_price(), Decimal('1.00'))


    def test_create_captured_charge(self):
        """ Test creating a test charge. """
        cl = self.__init_stripe()
        charge_id = cl.create_charge(self.card)
        self.assertEquals(charge_id, cl.stripe_id)
        # test charge retrieval!
        self.assertTrue(cl.retrieve_charge(id=charge_id))
        # charge is already captured!
        self.assertRaises(cl.capture_charge(), Exception)

    def test_create_uncaptured_charge(self):
        """ Create an uncaptured charge by passing kwarg."""
        cl = self.__init_stripe()
        charge_id = cl.create_charge(self.card, captured=False)
        self.assertEquals(charge_id, cl.stripe_id)
        # test charge retrieval!
        self.assertTrue(cl.retrieve_charge(id=charge_id))
        self.assertTrue(charge)
        # charge is already captured!
        cl.capture_charge()

    def test_refund(self):
        """ Test refunding an order """
        cl = self.__init_stripe()
        charge_id = cl.create_charge(self.card, captured=True)
        charge = cl.retrieve_charge(id=charge_id)
        self.assertTrue(charge)
        # refunds the most recent
        result = self.assertTrue(cl.refund_charge(charge=charge))



