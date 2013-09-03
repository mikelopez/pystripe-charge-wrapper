pystripe-charge-wrapper
------------------------------


[![Build Status](https://secure.travis-ci.org/mikelopez/pystripe-charge-wrapper.png?branch=master)](http://travis-ci.org/mikelopez/pystripe-charge-wrapper)



On ``refund_charge()``, ``capture_charge()``, ``create_charge()`` and ``retrieve_charge()`` methods, you can pass an optional id parameter to perform on a specific Charge. If you do not, it will use the last charge created, or the last order that was retrieved.

Run the tests
-------------



It is recommended to make a habit of always passing the ID parameter and/or calling retrieve_charge on a specific Charge that you want to work on.


IMPORTANT NOTE
---------------
If you do not pass an ID parameter to retrieve, it will use the LAST charge that was created or retrieved. (Yes, I'm being repetitive for a reason)


