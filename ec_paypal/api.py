import requests
from collections import OrderedDict
from .config import config
from .exceptions import PayPalError, PayPalFailure
from .fields import PayPalFields
from .utils import querystring_to_dict, drop_empty_values

__all__ = ['set_express_checkout', 'get_express_checkout_details', 'do_express_checkout_payment']


def call(method, fields=None, **kwargs):
    """
    DOCS: developer.paypal.com/webapps/developer/docs/classic/express-checkout/integration-guide/ECGettingStarted/
    """
    params = {
        'USER': config.USERNAME,
        'PWD': config.PASSWORD,
        'SIGNATURE': config.SIGNATURE,
        'VERSION': config.API_VERSION,
        'METHOD': method,
    }

    params.update(fields or kwargs)

    # Drop "empty" params
    drop_empty_values(params)

    # Sort params
    params = OrderedDict(((param, params[param]) for param in sorted(params)))

    # Call PayPal
    r = requests.get(config.API_URL, params=params)

    if r.status_code == 200:
        response_params = querystring_to_dict(r.content)
        response = PayPalFields.from_params(response_params)
        if response.success:
            return response
        else:
            raise PayPalFailure(response.error.message or 'Unknown error', response)
    else:
        raise PayPalError('HTTP%s' % r.status_code)


def set_express_checkout(fields):
    """
    DOCS: developer.paypal.com/webapps/developer/docs/classic/api/merchant/SetExpressCheckout_API_Operation_NVP/
    """
    return call('SetExpressCheckout', fields)


def get_express_checkout_details(token):
    """
    DOCS: developer.paypal.com/webapps/developer/docs/classic/api/merchant/GetExpressCheckoutDetails_API_Operation_NVP/
    """
    return call('GetExpressCheckoutDetails', TOKEN=token)


def do_express_checkout_payment(fields):
    """
    DOCS: developer.paypal.com/webapps/developer/docs/classic/api/merchant/DoExpressCheckoutPayment_API_Operation_NVP/
    """
    return call('DoExpressCheckoutPayment', fields)
