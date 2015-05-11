import urllib.parse
import base64
import json

from django.conf import settings
from django.core.urlresolvers import reverse
import requests
import six


class PayUApi():
    __BASE_URL = "https://secure.payu.com"
    __ORDER_URL = urllib.parse.urljoin(__BASE_URL, "api/v2_1/orders")

    @staticmethod
    def __get_signature():
        sig = "{}:{}".format(settings.DJANGO_PAY_PAYU_POS_ID, settings.DJANGO_PAY_PAYU_POS_AUTHORIZATION_KEY)
        sig = base64.encodebytes(six.b(sig))
        sig = b"Basic " + sig
        sig = sig.strip()
        return sig

    def make_order(self, request, payu_payment):
        url = self.__ORDER_URL
        data = {
            "notifyUrl": "{}{}".format(
                settings.BASE_URL,
                reverse('django_pay_payu_notify')
            ),
            "continueUrl": "{}{}".format(
                settings.BASE_URL,
                reverse('django_pay_payu_continue', args=[payu_payment.uid])
            ),
            "customerIp": request.META.get("REMOTE_ADDR"),
            "merchantPosId": settings.DJANGO_PAY_PAYU_POS_ID,
            "description": "Your order description",
            "currencyCode": "PLN",
            "totalAmount": str(int(100 * payu_payment.price_total)),
            "extOrderId": payu_payment.uid,
            "buyer": {
                "email": payu_payment.user.email,
                "firstName": payu_payment.user.first_name,
                "lastName": payu_payment.user.last_name,
            },
            "products": [
                {
                    "name": payu_payment.product.name,
                    "unitPrice": str(int(100 * payu_payment.product.price_total)),
                    "quantity": str(payu_payment.quantity),
                }
            ]
        }

        headers = {
            "Authorization": self.__get_signature(),
            "Content-Type": "application/json",
        }
        response = requests.post(url, data=json.dumps(data), headers=headers, allow_redirects=False)
        return response.status_code, response.content