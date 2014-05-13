class PayPalError(Exception):
    pass


class PayPalFailure(PayPalError):

    def __init__(self, message, response):
        super(PayPalFailure, self).__init__(message)
        self.response = response
