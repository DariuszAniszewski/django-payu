from djangopay.helpers import DjangoPayException, BadRequestJsonResponse


class DjangoPayExceptionsMiddleware(object):
    def process_exception(self, request, exception):
        if not isinstance(exception, DjangoPayException):
            return None
        return BadRequestJsonResponse({"error": exception.message})
