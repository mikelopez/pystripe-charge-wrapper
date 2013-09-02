from unittest import TestCase, TestSuite, TestTextRunner
from decimal import Decimal

try:
    import test_settings
except ImportError:
    raise Exception("No test_settings found. Need API Keys")
    sys.exit(1)

class TestStripeCharges(TestCase):
    """Test the stripe charge functionality."""

    stripe_api_key = getattr(settings, "stripe_api_key")
    def setUp(self):
        if not self.stripe_api_key:
            raise Exception("No valid api key found.")
            sys.exit(1)

    def test_charge(self):
        """Test the charges."""
        cl = StripeCharges(stripe_api_key=self.stripe_api_key)
        self.assertEquals(getattr(cl, "stripe_api_key"), getattr(self, "stripe_api_key"))

        cl.set_price('1.00')
        self.assertEquals(cl.get_price(), Decimal('1.00'))

