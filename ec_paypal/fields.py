import json
from .mapping import PayPalParamsTemplate
from .config import config
from .utils import DotDict, wrap_dicts_recursive, expand_dict, collapse_dict


class PayPalFields(DotDict, PayPalParamsTemplate):

    def __init__(self, iterable=None, **kwargs):
        """
        Initialize hierarchical fields dict and wrap recursive dicts to dot-dicts.
        """
        items = wrap_dicts_recursive(iterable or kwargs, DotDict)
        super(PayPalFields, self).__init__(items)

    @classmethod
    def from_params(cls, params):
        """
        Parse flat params dict and instantiate hierarchical fields dict.
        """
        fields = expand_dict(params, cls.template)
        return cls(fields)

    def fields(self):
        """
        Convert hierarchical fields dict to flat params dict.
        """
        return dict(collapse_dict(self, self.template))

    @classmethod
    def loads(cls, string):
        """
        Load json to hierarchical fields dict.
        """
        params = json.loads(string)
        return cls.from_params(params)

    def dumps(self):
        """
        Dump hierarchical fields dict to json.
        """
        return json.dumps(self)

    @property
    def success(self):
        """
        Shortcut for success ack status
        """
        return (self.status or '').upper() == 'SUCCESS'

    @property
    def redirect_url(self):
        """
        Render express checkout redirect url for token/id field
        """
        if self.id:
            return config.CHECKOUT_URL.format(token=self.id)

    @property
    def invoice(self):
        """
        Shortcut for invoice tracking number.
        """
        try:
            return self.transactions[0].tracking.invoice
        except (AttributeError, IndexError):
            return None


    @property
    def error(self):
        """
        Shortcut for errors dot-dict
        """
        try:
            return self.errors[0]
        except (AttributeError, IndexError):
            return DotDict()


class Payment(PayPalFields):

    def fields(self):
        """
        Sum item and detail amounts and format all amounts to strings.
        Convert hierarchical fields dict to flat params dict.
        """
        # Sum amounts
        for transaction in self.transactions:
            amount = transaction.amount
            if not amount.details.subtotal:
                items = transaction.item_list.get('items')
                subtotal = sum(float(item.price or 0) * (item.quantity or 1) for item in items)
                amount.details['subtotal'] = subtotal
            if not amount.total:
                amount['total'] = sum(float(amount) if amount is not None else float(0)
                                      for amount in amount.details.values())

        # Convert to params
        fields = super(Payment, self).fields()

        # Format amounts
        for key, value in fields.items():
            if 'AMT' in key:
                amount = float(value) if value is not None else float(0)
                fields[key] = '{:,.2f}'.format(amount)

        return fields
