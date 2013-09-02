from unittest import TestCase, TestSuite, TextTestRunner
from decimal import Decimal

from test_charges import TestStripeCharges

if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestStripeCharges('test_charge'))
    suite.addTest(TestStripeCharges('test_create_captured_charge'))
    suite.addTest(TestStripeCharges('test_create_uncaptured_charge'))
    suite.addTest(TestStripeCharges('test_refund'))
    TextTestRunner(verbosity=2).run(suite)


