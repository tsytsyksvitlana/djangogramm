import typing as t

from rest_framework.response import Response
from rest_framework import status


class BadResponse(Response):
    def __init__(self, data: t.Any) -> None:
        super().__init__(data, status=status.HTTP_400_BAD_REQUEST)
