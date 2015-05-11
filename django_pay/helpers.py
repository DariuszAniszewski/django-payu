from django.http.response import JsonResponse


class BadRequestJsonResponse(JsonResponse):
    status_code = 400


class DjangoPayException(Exception):
    def __init__(self, message):
        self.message = message


class NoParamException(DjangoPayException):
    pass


class BadParamValueException(DjangoPayException):
    pass


class PaymentStatus:
    STATUS_NEW = "new"
    STATUS_STARTED = "started"
    STATUS_FAILED = "failed"
    STATUS_COMPLETED = "completed"

    @staticmethod
    def all():
        return [
            PaymentStatus.STATUS_NEW,
            PaymentStatus.STATUS_STARTED,
            PaymentStatus.STATUS_FAILED,
            PaymentStatus.STATUS_COMPLETED,
        ]


class ErrorMessages():
    PAYMENT_NOT_FOUND = "payment not found"
    ORDER_ID_NOT_FOUND = "orderId not found"
    STATUS_NOT_FOUND = "status not found"
    EXT_ORDER_ID_NOT_FOUND = "extOrderId not found"
    BAD_JSON_STRUCTURE = "bad JSON structure"
    QUANTITY_NOT_FOUND = "quantity not found"
    PRODUCT_NOT_FOUND = "product not found"
    PRODUCT_ID_NOT_FOUND = "product_id not found"
    USER_NOT_FOUND = "user not found"
    USER_ID_NOT_FOUND = "user_id not found"
    EMPTY_JSON_RESPONSE = "empty JSON"
    EMPTY_REQUEST_RESPONSE = "empty request"
    NOT_A_JSON_RESPONSE = "not a JSON"