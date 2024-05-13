from rest_framework import status

from exception_handlers.base import BaseException


class CommentNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Comment with {id} not found'

    def __init__(self, comment_id: int) -> None:
        self.message = self.message.format(id=comment_id)
        super().__init__(self.message)
