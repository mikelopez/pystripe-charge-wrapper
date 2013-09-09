pystripe-charge-wrapper
========================

Simple class to create a charges on a card, and create a temporary customer object related to it. 
It currently supports creating captured/uncaptured charges, retrieving charges and details, issuing a refund and capturing an uncaptured charge.


.. image:: https://secure.travis-ci.org/mikelopez/pystripe-charge-wrapper.png?branch=master
    :target: http://travis-ci.org/mikelopez/pystripe-charge-wrapper


On ``refund_charge()``, ``capture_charge()``, ``create_charge()`` and ``retrieve_charge()`` methods, you can pass an optional id parameter to perform on a specific Charge. If you do not, it will use the last charge created, or the last order that was retrieved.



Run the tests with your api key
-------------------------------

Create a file called test_settings.py in your tests/ directory and set your ``TEST_STRIPE_SECRET`` Then run the test with ``python runner.py``



IMPORTANT NOTE
----------------
If you do not pass an ID parameter to retrieve, it will use the LAST charge that was created or retrieved. (Yes, I'm being repetitive for a reason)



Install requirements
----------------------

 ``pip install -r requirements.txt --use-mirrors``



Usage Samples
--------------

The basic scenario is to instantiate the class, set the price, and perform a charge (captured or uncaptured), or you can retrieve a charge to refund it or capture() it.
By default, it creates uncaptured charges to later capture them.

It is recommended to make a habit of always passing the ID parameter and/or calling retrieve_charge on a specific Charge that you want to work on.


Retrieving a charge
--------------------

You can retrieve a charge to check the status or get any other information on it
that the API defines.

.. code-block:: python 

    from pystripe_charge_wrapper.pystripe_charges import *
    cl = StripeCharges(stripe_api_key='abc123456fku')
    stripe_charge_id = cl.retrieve_charge(id='stripe-charge-id')
    # get the stripe id....
    sid = cl.stripe_id



Creating a captured charge
---------------------------

Create a captured charge (charge it immediately) by passing ``capture=True``. Leaving this value false or empty will default to False. When creating a charge, it will set the return stripe_id and stripe_object to the class (self)


.. code-block:: python

    from pystripe_charge_wrapper.pystripe_charges import *
    card = {'number': '4242424242424242', 'exp_month': '01', 
            'exp_year': '2016', 'cvc': '222'}
    cl = StripeCharges(stripe_api_key='abc123456fku')
    cl.set_price('1.00')
    stripe_charge_id = cl.create_charge(card=card, capture=True)



Creating an uncaptured charge
-----------------------------

To create an uncaptured charge, all you need to do different is to pass ``capture=False`` or just leave it out entirely. The default capture value is False


.. code-block:: python

    from pystripe_charge_wrapper.pystripe_charges import *
    card = {'number': '4242424242424242', 'exp_month': '01', 
            'exp_year': '2016', 'cvc': '222'}
    cl = StripeCharges(stripe_api_key='abc123456fuku')
    cl.set_price('1.00')
    stripe_charge_id = cl.create_charge(capture=False)



Setting a refund
-----------------

When setting a refund, you can explicitly pass the charge_id with the ``id`` argument, or you can leave it empty to use the last charge created (or order that was retrieved). It is better practice to just pass the id unless you're cool.


.. code-block:: python

    from pystripe_charge_wrapper.pystripe_charges import *
    cl = StripeCharges(stripe_api_key='abc123456fuku')
    stripe_object = cl.refund_charge(id='some-long-id')
    # stripe_object.get('refunded') will be True



Capturing an uncaptured charge
------------------------------

You can capture a charge later that was created uncaptured (for card authorization purposes).
Like all the other functions, you can explicitly define the ID of the charge you want to capture, or it will get the last charge that was created or retrieved from self


.. code-block:: python

    from pystripe_charge_wrapper.pystripe_charges import *
    cl = StripeCharges(stripe_api_key='abc123456fuku')
    stripe_object = cl.capture_charge(id='some-long-id')
    stripe_object.capture()
    # stripe_object.get('captured') will be True


