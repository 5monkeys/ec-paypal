class Config(dict):

    def __init__(self, iterable=None, **kwargs):
        super(Config, self).__init__(iterable, **kwargs)
        self._configured = False

    def get_paypal_domain(self):
        return 'sandbox.paypal.com' if self.SANDBOX else 'paypal.com'

    @property
    def API_URL(self):
        return 'https://api-3t.%s/nvp' % self.get_paypal_domain()

    @property
    def CHECKOUT_URL(self):
        return 'https://www.%s/cgi-bin/webscr?cmd=_express-checkout&token={token}' % self.get_paypal_domain()

    def from_dict(self, conf=None, **kwargs):
        self.update((conf or kwargs))

    def from_object(self, obj):
        conf = {key: getattr(obj, key) for key in dir(obj) if key.isupper()}
        self.update(conf)

    def update(self, other=None, **kwargs):
        super(Config, self).update(other, **kwargs)
        self._configured = True

    def is_configured(self):
        return self._configured

    __getattr__ = dict.__getitem__


config = Config({
    'SANDBOX': True,
    'API_VERSION': 109,
})
