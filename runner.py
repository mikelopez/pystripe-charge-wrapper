import sys
import unittest
from unittest import TestCase, TestSuite, TextTestRunner
from decimal import Decimal

sys.path.append('pystripe_charge_wrapper')
sys.path.append('pystripe_charge_wrapper/tests')

from test_charges import TestStripeCharges

if __name__ == '__main__':
    unittest.main()
    #suite = TestSuite()
    #suite.addTest(TestStripeCharges('test_charge'))
    #suite.addTest(TestStripeCharges('test_create_captured_charge'))
    #suite.addTest(TestStripeCharges('test_create_uncaptured_charge'))
    #suite.addTest(TestStripeCharges('test_refund'))
    #TextTestRunner(verbosity=2).run(suite)


