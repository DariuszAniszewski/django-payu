import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_payu.helpers import ErrorMessages, PaymentStatus
from django_payu.models import PayuPayment


class DjangoPayTestCase(TestCase):
    url = None

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

    def execute_get_request_and_expect_error(self, error):
        response = self.client.get(self.url)
        self.assertEqual(400, response.status_code)
        parsed_response = self.get_parsed_response(response)
        self.assertIn("error", parsed_response)
        self.assertEqual(error, parsed_response["error"])

    def execute_get_ajax_request_and_expect_error(self, error):
        response = self.client.get(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
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
        self.payment.name = "Test product"
        self.payment.price = 1000
        self.payment.quantity = 1
        self.payment.ip_address = "127.0.0.1"
        self.payment.save()

    def get_json_response_for_post_request(self, data):
        response = self.perform_json_post_request(data)
        self.assertEqual(200, response.status_code)
        response_dict = json.loads(response.content.decode("utf-8"))
        return response_dict

    def get_json_response_for_ajax_get_request(self):
        response = self.client.get(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        response_dict = json.loads(response.content.decode("utf-8"))
        return response_dict


class CommonPostTests:
    def test_get_request(self):
        response = self.perform_get_request()
        self.assertEqual(405, response.status_code)

    def test_with_empty_body(self):
        self.execute_post_request_and_expect_error("", ErrorMessages.EMPTY_REQUEST_RESPONSE)

    def test_with_non_json_body(self):
        self.execute_post_request_and_expect_error("not_a_json", ErrorMessages.NOT_A_JSON_RESPONSE)

    def test_with_empty_json(self):
        self.execute_post_request_and_expect_error("{}", ErrorMessages.EMPTY_JSON_RESPONSE)


class TestCreateNewPayuPayment(DjangoPayTestCase, CommonPostTests):
    def setUp(self):
        self.url = reverse('django_pay_payu_start')

    def test_with_no_user_id(self):
        self.execute_post_request_and_expect_error(
            json.dumps({
                "some": "field",
            }),
            ErrorMessages.USER_ID_NOT_FOUND
        )

    def test_with_no_quantity(self):
        self.execute_post_request_and_expect_error(
            json.dumps({
                "user_id": 1,
                "product_id": 1,
            }),
            ErrorMessages.QUANTITY_NOT_FOUND
        )

    def test_with_bad_user_id(self):
        self.execute_post_request_and_expect_error(
            json.dumps({
                "user_id": -1,
                "product_id": 1,
                "quantity": 1,
                "title": "Product name",
                "price": 100,
            }),
            ErrorMessages.USER_NOT_FOUND
        )

    def test_with_no_price(self):
        self.create_user()

        self.execute_post_request_and_expect_error(json.dumps({
            "user_id": self.user.pk,
            "quantity": 1,
            "title": "Product name",
        }), ErrorMessages.PRICE_NOT_FOUND)

    def test_with_no_title(self):
        self.create_user()

        self.execute_post_request_and_expect_error(json.dumps({
            "user_id": self.user.pk,
            "quantity": 1,
            "price": 1,
        }), ErrorMessages.TITLE_NOT_FOUND)

    def test_with_wrong_price(self):
        self.create_user()

        self.execute_post_request_and_expect_error(json.dumps({
            "user_id": self.user.pk,
            "quantity": 1,
            "price": "not_an_int",
            "title": "Product name",
        }), ErrorMessages.PRICE_MALFORMED)

    def test_with_wrong_quantity(self):
        self.create_user()

        self.execute_post_request_and_expect_error(json.dumps({
            "user_id": self.user.pk,
            "quantity": "not_an_int",
            "title": "Product name",
            "price": 100,
        }), ErrorMessages.QUANTITY_MALFORMED)

    def test_payment_created(self):
        self.create_user()

        response_dict = self.get_json_response_for_post_request(json.dumps({
            "user_id": self.user.pk,
            "price": 100,
            "title": "Product name",
            "quantity": 1,
        }))
        self.assertIn("payu_id", response_dict)
        self.assertIn("order_id", response_dict)
        self.assertIn("follow", response_dict)
        self.assertTrue(PayuPayment.objects.filter(
            pk=response_dict["order_id"],
            payu_id=response_dict["payu_id"]
        ).exists())


class TestPayuPaymentNotification(DjangoPayTestCase, CommonPostTests):
    def setUp(self):
        self.url = reverse('django_pay_payu_notify')


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
                "extOrderId": self.payment.uid,
                "status": "PENDING"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))
        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_STARTED, self.payment.status)

    def test_payment_completed(self):
        self.create_payment()
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.uid,
                "status": "COMPLETED"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))
        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_COMPLETED, self.payment.status)

    def test_payment_cancelled(self):
        self.create_payment()
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.uid,
                "status": "CANCELED"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))
        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_FAILED, self.payment.status)

    def test_payment_completed_then_pending(self):
        self.create_payment()

        # mark Payment as completed
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.uid,
                "status": "COMPLETED"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))

        # then mark Payment as pending
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.uid,
                "status": "PENDING"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))

        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_COMPLETED, self.payment.status)

    def test_payment_failed_then_pending(self):
        self.create_payment()

        # mark Payment as completed
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.uid,
                "status": "CANCELED"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))

        # then mark Payment as pending
        data = {
            "order": {
                "orderId": self.payment.payu_id,
                "extOrderId": self.payment.uid,
                "status": "PENDING"
            }
        }
        self.get_json_response_for_post_request(json.dumps(data))

        self.payment.refresh_from_db()
        self.assertEqual(PaymentStatus.STATUS_FAILED, self.payment.status)


class TestPayuPaymentStatus(DjangoPayTestCase):
    def setUp(self):
        self.create_payment()
        self.url = reverse('django_pay_payu_status', args=[self.payment.pk])

    def test_get_status_of_not_existing_payment(self):
        self.url = reverse('django_pay_payu_status', args=["dummy_payment"])
        self.execute_get_ajax_request_and_expect_error(ErrorMessages.PAYMENT_NOT_FOUND)

    def test_get_status_not_as_ajax(self):
        self.execute_get_request_and_expect_error(ErrorMessages.NOT_AJAX_REQUEST)

    def test_get_status_of_existing_payment(self):
        for status in PaymentStatus.all():
            self.payment.status = status
            self.payment.save()
            json_response = self.get_json_response_for_ajax_get_request()
            self.assertIn("status", json_response)
            self.assertEqual(status, json_response["status"])

