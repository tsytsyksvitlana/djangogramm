import typing as t

from django.db.models import (
    Count,
    Exists,
    Prefetch,
    QuerySet
)
from django.contrib.contenttypes.models import ContentType

from rest_framework import (
    generics,
    mixins
)
from rest_framework.request import Request
from rest_framework.response import Response

from utils.responses.success import (
    OkResponse,
    DeleteResponse,
    CreateResponse
)
from exception_handlers.base import NotRequiredData
from exception_handlers.post import UserNotFound, PostNotFound
from exception_handlers.comment import CommentNotFound
from comment.api.serializers import CommentSerializer
from comment.models.comment import Comment
from post.models.like import Like
from post.models.post import Post
from user_profile.models.user import User


class CommentBaseAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    serializer_class = CommentSerializer

    def get_queryset(self) -> QuerySet[Comment]:
        user = t.cast(User, self.request.user)
        like_comm = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Comment)
        )

        sub_query = Like.objects.annotate(
            count_likes=Count('likes'),
            api_is_liked=Exists(like_comm),
        ).annotate(is_liked=Exists(User.objects.filter(id=user.id)))

        likes = Prefetch('likes', queryset=sub_query)
        return Comment.objects.prefetch_related(likes)

    def get(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        return self.create(request, *args, **kwargs)


class CommentViewPost(CommentBaseAPIView):
    def get_queryset(self) -> QuerySet[Comment]:
        queryset = super().get_queryset().filter(
            post=self.kwargs['post_id'], id=self.kwargs['comment_id']
        )
        return queryset


class CommentAPIView(CommentBaseAPIView):
    def post(self, request: Request, post_id: int) -> Response:
        if (user_id := request.user.id) is None:
            raise NotRequiredData
        if (text := request.data.get('text')) is None:
            raise NotRequiredData
        if (user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        if (post := Post.objects.filter(id=post_id).first()) is None:
            raise PostNotFound(post_id)
        new_comment = Comment.objects.create(
            text=text, user=user, post=post
        )
        return CreateResponse({'id': new_comment.id})


class CommentByIdAPIView(CommentViewPost):
    def get(self, request: Request, post_id: int, comment_id: int) -> Response:
        queryset = self.get_queryset().filter(id=comment_id)
        if not queryset.exists():
            raise CommentNotFound(comment_id)
        serialize = self.get_serializer(queryset, many=True)
        return OkResponse(serialize.data)

    def put(self, request: Request, post_id: int, comment_id: int) -> Response:
        new_text = request.data.get('text')
        if not new_text:
            raise NotRequiredData
        comment = Comment.objects.filter(id=comment_id, post=post_id).first()
        if comment is None:
            raise CommentNotFound(comment_id)

        comment.text = new_text
        comment.save()
        return OkResponse({'message': 'Comment updated successfully'})

    def delete(
        self, request: Request, post_id: int, comment_id: int
    ) -> Response:
        Comment.objects.filter(
            id=comment_id, post=post_id, user=request.user
        ).delete()
        return DeleteResponse()


class AllCommentsForUserAPIView(CommentBaseAPIView):
    def get(self, request: Request, user_id: int) -> Response:
        if (user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        queryset = super().get_queryset().filter(user=user)
        serialize = self.get_serializer(queryset, many=True)
        return OkResponse(serialize.data)


class AllMyCommentsAPIView(AllCommentsForUserAPIView):
    def get(self, request: Request) -> Response:
        return super().get(request, request.user.id)
