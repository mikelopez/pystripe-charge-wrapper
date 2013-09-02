import os
import sys

PATH_APPEND = os.path.realpath(os.path.dirname(__file__))
#sys.path.append('../')

from test_charges import TestStripeCharges

if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestStripeCharges('test_charge'))
    TextTestRuner(verbosity=2).run(suite)


