import json

from django.http.response import HttpResponseBadRequest
from django_pay.helpers import BadRequestJsonResponse, ErrorMessages


def require_JSON(func):
    def wrap(request, *args, **kwargs):
        body = request.body.decode('utf-8')
        if not body:
            return BadRequestJsonResponse({"error": ErrorMessages.EMPTY_REQUEST_RESPONSE})
        try:
            data = json.loads(body)
        except ValueError:
            return BadRequestJsonResponse({"error": ErrorMessages.NOT_A_JSON_RESPONSE})

        if not data:
            return BadRequestJsonResponse({"error": ErrorMessages.EMPTY_JSON_RESPONSE})
        return func(request, *args, **kwargs)

    return wrap


def require_AJAX(func):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return func(request, *args, **kwargs)

    return wrap