from django_payu.helpers import DjangoPayException, BadRequestJsonResponse


class DjangoPayExceptionsMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, DjangoPayException):
            return BadRequestJsonResponse({"error": exception.message})
