ec-paypal
=========

Easy PayPal Express Checkout using the Classic APIs for full feature set, mimicking the REST APIs.


Django example
--------------
See mapping.py for complete payment structure

```python
# settings.py
import ec_paypal as paypal

paypal.config.from_dict({
    'SANDBOX': True,
    'USERNAME': 'username',
    'PASSWORD': 'password',
    'SIGNATURE': 'signature',
})
```


```python
# views.py
import ec_paypal as paypal

def pay(request):
    order = Order.objects...

    payment = paypal.Payment({
        'intent': 'Sale',
        'transactions': [{
            'tracking': {'invoice': order.reference},
            # 'ipn_url': '...',
            'category': 2,
            'item_list': {
                'items': [{
                    'name': item.description,
                    'price': item.amount,
                    'quantity': item.qty
                } for item in order.items.all],
            },
            'amount': {
                'currency': 'SEK',
                # 'details': {
                #     'shipping': 50,
                #     'shipping_discount': -50
                # }
            }
        }],
        'redirect_urls': {
            'return_url': settings.PAYPAL_RETURN_URL,
            'cancel_url': settings.PAYPAL_CANCEL_URL,
        },
        'page': {
            'locale': 'sv_SE',
            'flow': 'Sole',
            'prompt': 'Billing',
            'shipping_address': 2,
            'layout': {
                'brand': 'My Example Store',
                'logo': 'http://example.com/img/logo.png',  # 190x60
                'cart_color': 'e5e5e5',
            }
        }
    })

    # Create payment
    response = paypal.set_express_checkout(payment.fields())

    # Persist/remember PayPal token: response.id

    # Redirect to PayPal
    return redirect(response.redirect_url)
```
