from test_base import *

from test_charges import TestStripeCharges

if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestStripeCharges('test_charge'))
    TextTestRuner(verbosity=2).run(suite)


