from rest_framework import status

from exception_handlers.base import BaseException


class PostNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Post not found {id}'

    def __init__(self, post_id: int) -> None:
        self.message = self.message.format(id=post_id)
        super().__init__(self.message)


class UserNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'User with {id} not found'

    def __init__(self, user_id: int) -> None:
        self.message = self.message.format(id=user_id)
        super().__init__(self.message)


class EnoughtFollowers(Exception):
    status_code = status.HTTP_409_CONFLICT
    message = 'You have already followed this user'
