import os
import base64


class GeneratePromoCodes:
    def __init__(self):
        self.len = 8

    def promo_code(self):
        token = os.urandom(self.len)
        return base64.b64encode(token)
