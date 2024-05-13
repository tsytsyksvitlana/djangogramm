from rest_framework import status


class BaseException(Exception):
    status_code: int
    message: str
    detail_info: str | bool = False


class NotRequiredData(Exception):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = 'Not all necessary data provided'
    detail_info = True


class NoAuthUser(Exception):
    status_code = status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED
    message = 'User have to be authenticated!'


class EnoughtLikes(Exception):
    status_code = status.HTTP_409_CONFLICT
    message = 'You have already liked this post'
