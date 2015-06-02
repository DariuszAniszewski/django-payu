import urllib.parse
import base64
import json

from django.conf import settings
from django.core.urlresolvers import reverse
import requests
import six


class PayUApi:
    __BASE_URL = "https://secure.payu.com"
    __ORDER_URL = urllib.parse.urljoin(__BASE_URL, "api/v2_1/orders")

    POS_ID = None
    POS_AUTHORIZATION_KEY = None

    def __init__(self, pos_id, pos_authorization_key):
        super().__init__()
        self.POS_ID = pos_id
        self.POS_AUTHORIZATION_KEY = pos_authorization_key

    def __get_signature(self):
        sig = "{}:{}".format(self.POS_ID, self.POS_AUTHORIZATION_KEY)
        sig = base64.encodebytes(six.b(sig))
        sig = b"Basic " + sig
        sig = sig.strip()
        return sig

    def make_order(self, payu_payment):
        data = {
            "notifyUrl": "{}{}".format(
                settings.DJANGO_PAYU_BASE_URL,
                reverse('django_pay_payu_notify')
            ),
            "continueUrl": payu_payment.continue_url,
            "customerIp": payu_payment.buyer_ip_address,
            "merchantPosId": self.POS_ID,
            "description": payu_payment.payment_description,
            "currencyCode": "PLN",
            "totalAmount": payu_payment.total_price,
            "extOrderId": payu_payment.payment_id,
            "buyer": {
                "email": payu_payment.buyer_email,
                "firstName": payu_payment.buyer_first_name,
                "lastName": payu_payment.buyer_last_name,
            },
            "products": [
                {
                    "name": payu_payment.product_name,
                    "unitPrice": payu_payment.product_unit_price,
                    "quantity": payu_payment.product_quantity,
                }
            ]
        }

        headers = {
            "Authorization": self.__get_signature(),
            "Content-Type": "application/json",
        }
        response = requests.post(self.__ORDER_URL, data=json.dumps(data), headers=headers, allow_redirects=False)
        return response.status_code, response.content