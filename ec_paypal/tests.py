# -*- coding: utf-8 -*-
from unittest import TestCase
import ec_paypal as paypal
from .fields import PayPalFields
from .utils import collapse_dict, expand_dict, querystring_to_dict, drop_empty_values, wrap_dicts_recursive, DotDict


class Test(TestCase):

    def test_config(self):
        self.assertFalse(paypal.config.is_configured())
        self.assertTrue(paypal.config.SANDBOX)
        paypal.config.from_dict(SANDBOX=False, USERNAME='test')
        self.assertTrue(paypal.config.is_configured())
        self.assertEqual(paypal.config.USERNAME, 'test')
        self.assertFalse(paypal.config.SANDBOX)

    def test_querystring_to_dict(self):
        d = querystring_to_dict('name=%C3%A5%C3%A4%C3%B6&param=value')
        self.assertDictEqual(d, dict(NAME=u'åäö', PARAM='value'))

    def test_collapse_expand_dict(self):
        mapping = {
            'amount': 'AMT',
            'data': {'key': {'a': 'VALUE_A', 'b': 'VALUE_B'}},
            'list': [{
                'parameter': 'LIST-{}-PARAM',
                'sublist': [{'name': 'LIST-{}-NAME-{}'}]
            }]
        }
        data = {
            'amount': 123,
            'data': {'key': {'a': 'A', 'b': 'B'}},
            'list': [{
                'parameter': 'value',
                'sublist': [{'name': 'bo'}, {'name': 'jonas'}, {'name': 'lundberg'}]
            }]
        }
        params = dict(collapse_dict(data, mapping))

        self.assertDictEqual(params, {
            'AMT': 123,
            'VALUE_A': 'A',
            'VALUE_B': 'B',
            'LIST-0-PARAM': 'value',
            'LIST-0-NAME-0': 'bo',
            'LIST-0-NAME-1': 'jonas',
            'LIST-0-NAME-2': 'lundberg'
        })

        data2 = expand_dict(params, mapping)

        self.assertDictEqual(data2, data)

    def test_dot_dict(self):
        d = DotDict({'a': 'b'})
        self.assertEqual(d.a, 'b')

    def test_drop_empty_values(self):
        d = {'a': 0, 'b': 1, 'c': None, 'd': '', 'e': 'e', 'f': u'ö'}
        drop_empty_values(d)
        remaining_keys = set(d.keys())
        self.assertSetEqual(remaining_keys, {'a', 'b', 'e', 'f'})

    def test_wrap_recursive(self):
        class FooDict(dict):
            pass

        d = {'a': 1,
             'b': {'foo': 'bar', 'ham': ['egg', {'x': 'y', 'z': {}}]},
             'c': [1, 2, [{'5': 'M'}]]}

        d = wrap_dicts_recursive(d, FooDict)

        self.assertEqual(type(d), FooDict)
        self.assertEqual(type(d['b']), FooDict)
        self.assertEqual(type(d['b']['ham'][1]), FooDict)
        self.assertEqual(type(d['b']['ham'][1]['z']), FooDict)
        self.assertEqual(type(d['c'][2][0]), FooDict)

    def test_payment(self):
        payment = paypal.Payment({
            'intent': 'Sale',
            'payer': {
                'payer_info': {
                    'email': 'jonas@5monkeys.se',
                }
            },
            'transactions': [{
                'item_list': {
                    'items': [{
                        'name': u'Banan',
                        'sku': 'BN',
                        'price': 6,
                        'currency': 'SEK',
                        'quantity': 2
                    }, {
                        'name': u'Kött',
                        'sku': 'WSKY',
                        'price': 23.5,
                        'currency': 'SEK',
                        'quantity': 1
                    }]
                },
                'amount': {
                    'details': {
                        'shipping': 5,
                        'shipping_discount': '-3.5',
                        'handling': 2,
                        'tax': 3,
                    }
                }
            }]
        })

        self.assertEqual(payment.intent, 'Sale')
        self.assertFalse(payment.max_amount)
        self.assertFalse(payment.transactions[0].amount.total)

        payment.transactions[0].description = 'foobar'
        self.assertEqual(payment.transactions[0].description, 'foobar')

        fields = payment.fields()
        self.maxDiff = None
        self.assertDictEqual(fields, {
            'EMAIL': 'jonas@5monkeys.se',
            'L_PAYMENTREQUEST_0_AMT0': '6.00',
            'L_PAYMENTREQUEST_0_AMT1': '23.50',
            'L_PAYMENTREQUEST_0_NAME0': u'Banan',
            'L_PAYMENTREQUEST_0_NAME1': u'Kött',
            'L_PAYMENTREQUEST_0_NUMBER0': 'BN',
            'L_PAYMENTREQUEST_0_NUMBER1': 'WSKY',
            'L_PAYMENTREQUEST_0_QTY0': 2,
            'L_PAYMENTREQUEST_0_QTY1': 1,
            'PAYMENTREQUEST_0_AMT': '42.00',
            'PAYMENTREQUEST_0_DESC': 'foobar',
            'PAYMENTREQUEST_0_CURRENCYCODE': 'SEK',
            'PAYMENTREQUEST_0_HANDLINGAMT': '2.00',
            'PAYMENTREQUEST_0_ITEMAMT': '35.50',
            'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
            'PAYMENTREQUEST_0_SHIPDISCAMT': '-3.50',
            'PAYMENTREQUEST_0_SHIPPINGAMT': '5.00',
            'PAYMENTREQUEST_0_TAXAMT': '3.00'
        })

    def test_get_details_response(self):
        response = '{"PAYMENTREQUEST_0_SHIPTOSTREET": "1 Main St", "ACK": "Success", "L_ITEMLENGTHVALUE1": "   0.00000", "SHIPTOCITY": "San Jose", "SHIPDISCAMT": "0.00", "PAYMENTREQUEST_0_ADDRESSSTATUS": "Confirmed", "PAYMENTREQUEST_0_INSURANCEAMT": "0.00", "PAYMENTREQUEST_0_SHIPTOCOUNTRYNAME": "United States", "EMAIL": "jonas+mirlo@5monkeys.se", "SHIPPINGAMT": "295.00", "TAXAMT": "0.00", "PAYMENTREQUEST_0_AMT": "5290.00", "PAYMENTREQUEST_0_HANDLINGAMT": "0.00", "PAYMENTREQUEST_0_TAXAMT": "0.00", "PAYMENTREQUESTINFO_0_ERRORCODE": "0", "L_QTY1": "1", "L_QTY0": "1", "PAYMENTREQUEST_0_SHIPTOZIP": "95131", "PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE": "US", "L_PAYMENTREQUEST_0_NAME1": "Orange", "L_PAYMENTREQUEST_0_NAME0": "Pink Solid", "PAYMENTREQUEST_0_CURRENCYCODE": "SEK", "TOKEN": "EC-5XY471680M084133N", "VERSION": "109", "PAYMENTREQUEST_0_SHIPDISCAMT": "0.00", "BUILD": "9285531", "L_PAYMENTREQUEST_0_AMT1": "0.00", "SHIPTOZIP": "95131", "PAYMENTREQUEST_0_SHIPTOSTATE": "CA", "FIRSTNAME": "Jonas", "L_PAYMENTREQUEST_0_ITEMWIDTHVALUE0": "   0.00000", "L_PAYMENTREQUEST_0_ITEMWIDTHVALUE1": "   0.00000", "PAYMENTREQUEST_0_SHIPPINGAMT": "295.00", "HANDLINGAMT": "0.00", "L_NAME1": "Orange", "L_NAME0": "Pink Solid", "L_PAYMENTREQUEST_0_QTY1": "1", "L_PAYMENTREQUEST_0_QTY0": "1", "LASTNAME": "Lundberg", "L_PAYMENTREQUEST_0_ITEMWEIGHTVALUE1": "   0.00000", "L_PAYMENTREQUEST_0_ITEMWEIGHTVALUE0": "   0.00000", "SHIPTONAME": "Jonas Lundberg", "L_TAXAMT1": "0.00", "ITEMAMT": "4995.00", "L_ITEMWEIGHTVALUE1": "   0.00000", "L_ITEMWEIGHTVALUE0": "   0.00000", "ADDRESSSTATUS": "Confirmed", "CORRELATIONID": "5d06d40aeaa77", "PAYMENTREQUEST_0_INVNUM": "6f184b7e36214e7ba61e91719c6fc529", "PAYMENTREQUEST_0_INSURANCEOPTIONOFFERED": "false", "PAYMENTREQUEST_0_SHIPTOCITY": "San Jose", "SHIPTOSTREET": "1 Main St", "L_ITEMLENGTHVALUE0": "   0.00000", "L_PAYMENTREQUEST_0_ITEMHEIGHTVALUE0": "   0.00000", "L_PAYMENTREQUEST_0_ITEMHEIGHTVALUE1": "   0.00000", "SHIPTOCOUNTRYNAME": "United States", "AMT": "5290.00", "PAYMENTREQUEST_0_ITEMAMT": "4995.00", "PAYERID": "TELLDSGUKEWZ8", "PAYMENTREQUEST_0_ADDRESSNORMALIZATIONSTATUS": "None", "COUNTRYCODE": "US", "CURRENCYCODE": "SEK", "L_PAYMENTREQUEST_0_ITEMLENGTHVALUE1": "   0.00000", "L_PAYMENTREQUEST_0_ITEMLENGTHVALUE0": "   0.00000", "PAYMENTREQUEST_0_SHIPTONAME": "Jonas Lundberg", "INVNUM": "6f184b7e36214e7ba61e91719c6fc529", "INSURANCEAMT": "0.00", "L_PAYMENTREQUEST_0_AMT0": "4995.00", "CHECKOUTSTATUS": "PaymentActionNotInitiated", "PAYERSTATUS": "verified", "L_ITEMHEIGHTVALUE0": "   0.00000", "L_ITEMHEIGHTVALUE1": "   0.00000", "L_ITEMWIDTHVALUE0": "   0.00000", "L_ITEMWIDTHVALUE1": "   0.00000", "TIMESTAMP": "2014-01-31T06:55:15Z", "SHIPTOSTATE": "CA", "L_TAXAMT0": "0.00", "SHIPTOCOUNTRYCODE": "US", "L_PAYMENTREQUEST_0_TAXAMT1": "0.00", "L_PAYMENTREQUEST_0_TAXAMT0": "0.00", "L_AMT1": "0.00", "L_AMT0": "4995.00"}'
        response = PayPalFields.loads(response)
        self.assertEqual(response.status, 'Success')
        self.assertTrue(response.success)
        self.assertEqual(response.invoice, '6f184b7e36214e7ba61e91719c6fc529')
        payer = response.payer.payer_info
        self.assertEqual(payer.first_name, 'Jonas')
        self.assertIsNone(payer.middle_name)
        self.assertEqual(payer.shipping_address.status, 'Confirmed')

    def todo_test_get(self):
        try:
            response = paypal.get_express_checkout_details('123')
        except Exception as e:
            self.assertEqual(e.response.status, 'Failed')
