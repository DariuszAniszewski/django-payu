import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_payu.core import Buyer, Product, DjangoPayU

from django_payu.helpers import ErrorMessages, PaymentStatus, DjangoPayException
from django_payu.models import PayuPayment


class TestBuyer(TestCase):
    def test_create_buyer(self):
        buyer = Buyer("first_name", "last_name", "email@server.com", "127.0.0.1")
        self.assertEqual("first_name", buyer.first_name)
        self.assertEqual("last_name", buyer.last_name)
        self.assertEqual("email@server.com", buyer.email)
        self.assertEqual("127.0.0.1", buyer.ip_address)

    def test_create_buyer_with_wrong_email(self):
        with self.assertRaises(DjangoPayException) as e:
            Buyer("first_name", "last_name", "email", "127.0.0.1")

        self.assertEqual(ErrorMessages.NOT_VALID_EMAIL_ADDRESS, e.exception.message)

    def test_create_buyer_with_wrong_ip_address(self):
        with self.assertRaises(DjangoPayException) as e:
            Buyer("first_name", "last_name", "email@server.com", "not_email")

        self.assertEqual(ErrorMessages.NOT_VALID_IP_ADDRESS, e.exception.message)


class TestProduct(TestCase):
    def test_create_product(self):
        product = Product("Test product", 100, 2)
        self.assertEqual("Test product", product.name)
        self.assertEqual(2, product.quantity)
        self.assertEqual(100, product.unit_price)

    def test_create_product_with_wrong_quantity(self):
        with self.assertRaises(DjangoPayException) as e:
            Product("Test product", 100, 3.4)

        self.assertEqual(ErrorMessages.NOT_VALID_QUANTITY, e.exception.message)

    def test_create_product_with_wrong_string_quantity(self):
        with self.assertRaises(DjangoPayException) as e:
            Product("Test product", 100, "3.4")

        self.assertEqual(ErrorMessages.NOT_VALID_QUANTITY, e.exception.message)

    def test_create_product_with_wrong_unit_price(self):
        with self.assertRaises(DjangoPayException) as e:
            Product("Test product", 10.4, 2)

        self.assertEqual(ErrorMessages.NOT_VALID_UNIT_PRICE, e.exception.message)

    def test_create_product_with_wrong_string_unit_price(self):
        with self.assertRaises(DjangoPayException) as e:
            Product("Test product", "10.4", 2)

        self.assertEqual(ErrorMessages.NOT_VALID_UNIT_PRICE, e.exception.message)


class TestNewPayment(TestCase):
    def setUp(self):
        self.product = Product("Test product", 100, 2)
        self.buyer = Buyer("first_name", "last_name", "email@server.com", "127.0.0.1")

    def test_payment_created(self):
        payment_id, follow_url = DjangoPayU.create_payu_payment(self.buyer, self.product, "payment description",
                                                                "localhost")
        self.assertIsNotNone(payment_id)
        self.assertIsNotNone(follow_url)


class TestGetPaymentStatus(TestCase):
    def setUp(self):
        self.product = Product("Test product", 100, 2)
        self.buyer = Buyer("first_name", "last_name", "email@server.com", "127.0.0.1")
        self.payment_id, self.follow_url = DjangoPayU.create_payu_payment(self.buyer, self.product, "test payment",
                                                                          "localhost")

    def test_get_payment_status_for_started_payment(self):
        self.assertEqual(DjangoPayU.get_payment_status(self.payment_id), PaymentStatus.STATUS_STARTED)

    def test_get_payment_status_for_failed_payment(self):
        PayuPayment.objects.filter(pk=self.payment_id).update(payment_status=PaymentStatus.STATUS_FAILED)
        self.assertEqual(DjangoPayU.get_payment_status(self.payment_id), PaymentStatus.STATUS_FAILED)

    def test_get_payment_status_for_completed_payment(self):
        PayuPayment.objects.filter(pk=self.payment_id).update(payment_status=PaymentStatus.STATUS_COMPLETED)
        self.assertEqual(DjangoPayU.get_payment_status(self.payment_id), PaymentStatus.STATUS_COMPLETED)


class TestPayuPaymentNotification(TestCase):
    url = None

    def setUp(self):
        self.url = reverse('django_pay_payu_notify')

    def perform_get_request(self):
        return self.client.get(self.url)

    def perform_json_post_request(self, data):
        return self.client.post(self.url, data=data, content_type="application/json")

    def get_parsed_response(self, response):
        return json.loads(response.content.decode('utf-8'))

    def execute_post_request_and_expect_error(self, data, error):
        response = self.perform_json_post_request(data)
        self.assertEqual(400, response.status_code)
        parsed_response = self.get_parsed_response(response)
        self.assertIn("error", parsed_response)
        self.assertEqual(error, parsed_response["error"])

    def create_user(self):
        self.user = User.objects.create()

    def create_payment(self):
        self.create_user()
        self.payment = PayuPayment()
        self.payment.payu_id = "payu-id"
        self.payment.user = self.user
        self.payment.product_name = "Test product"
        self.payment.product_unit_price = 1000
        self.payment.product_quantity = 1
        self.payment.buyer_ip_address = "127.0.0.1"
        self.payment.save()

    def get_json_response_for_post_request(self, data):
        response = self.perform_json_post_request(data)
        self.assertEqual(200, response.status_code)
        response_dict = json.loads(response.content.decode("utf-8"))
        return response_dict

    def test_get_request(self):
        response = self.perform_get_request()
        self.assertEqual(405, response.status_code)

    def test_with_empty_body(self):
        self.execute_post_request_and_expect_error("", ErrorMessages.EMPTY_REQUEST_RESPONSE)

    def test_with_non_json_body(self):
        self.execute_post_request_and_expect_error("not_a_json", ErrorMessages.NOT_A_JSON_RESPONSE)

    def test_with_empty_json(self):
        self.execute_post_request_and_expect_error("{}", ErrorMessages.EMPTY_JSON_RESPONSE)

    def test_order_key_not_found(self):
        data = {"bad": {}}
        self.execute_post_request_and_expect_error(json.dumps(data), ErrorMessages.BAD_JSON_STRUCTURE)

    def test_order_id_not_in_json(self):
        data = {"order": {}}
        self.execute_post_request_and_expect_error(json.dumps(data), ErrorMessages.ORDER_ID_NOT_FOUND)

    def test_ext_order_id_not_in_json(self):
        data = {"order": {"orderId": "some_order_id"}}
        self.execute_post_request_and_expect_error(json.dumps(data), ErrorMessages.EXT_ORDER_ID_NOT_FOUND)

    def test_status_not_in_json(self):
        data = {"order": {"orderId": "some_order_id", "extOrderId": "some_ext"}}
        self.execute_post_request_and_expect_error(json.dumps(data), ErrorMessages.STATUS_NOT_FOUND)

    def test_payment_not_found(self):
        data = {"order": {"orderId": "some_order_id", "extOrderId": "some_ext", "status": "some_status"}}
        self.execute_post_request_and_expect_error(json.dumps(data), ErrorMessages.PAYMENT_NOT_FOUND)

    def test_payment_started(self):
        self.create_payment()
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.payment_id,
                "status": "PENDING"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))
        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_STARTED, self.payment.payment_status)

    def test_payment_completed(self):
        self.create_payment()
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.payment_id,
                "status": "COMPLETED"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))
        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_COMPLETED, self.payment.payment_status)

    def test_payment_cancelled(self):
        self.create_payment()
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.payment_id,
                "status": "CANCELED"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))
        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_FAILED, self.payment.payment_status)

    def test_payment_completed_then_pending(self):
        self.create_payment()

        # mark Payment as completed
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.payment_id,
                "status": "COMPLETED"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))

        # then mark Payment as pending
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.payment_id,
                "status": "PENDING"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))

        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_COMPLETED, self.payment.payment_status)

    def test_payment_failed_then_pending(self):
        self.create_payment()

        # mark Payment as completed
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.payment_id,
                "status": "CANCELED"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))

        # then mark Payment as pending
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.payment_id,
                "status": "PENDING"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))

        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_FAILED, self.payment.payment_status)