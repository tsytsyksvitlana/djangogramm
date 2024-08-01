import typing as t

from rest_framework.response import Response
from rest_framework import status


class OkResponse(Response):
    def __init__(self, data: t.Any) -> None:
        super().__init__(data, status=status.HTTP_200_OK)


class SuccessResponse(Response):
    def __init__(self) -> None:
        super().__init__(status=status.HTTP_200_OK)


class CreateResponse(Response):
    def __init__(self, data: t.Any) -> None:
        super().__init__(data, status=status.HTTP_201_CREATED)


class DeleteResponse(Response):
    def __init__(self, data: t.Any = None) -> None:
        if data:
            super().__init__(data, status=status.HTTP_204_NO_CONTENT)
        else:
            super().__init__(status=status.HTTP_204_NO_CONTENT)
