import logging
import typing as t

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from exception_handlers.base import BaseException


log = logging.getLogger(__name__)


def custom_exception_handler(
        exc: type[BaseException] | Exception, context: dict[str, t.Any]
) -> Response:
    exc = t.cast(Exception, exc)
    if isinstance(exc, BaseException):
        if exc.detail_info:
            return Response(
                {'error': exc.message, 'detail': context},
                status=exc.status_code
            )
        return Response({'error': exc.message}, status=exc.status_code)
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    log.error("Unhandled exception %s", exc, exc_info=exc)
    return Response({'error': 'Unknown'}, status=status.HTTP_400_BAD_REQUEST)
