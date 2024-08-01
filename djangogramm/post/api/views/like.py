from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    Q
)

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.responses.success import (
    SuccessResponse,
    OkResponse,
    CreateResponse,
    DeleteResponse
)
from exception_handlers.base import NotRequiredData, EnoughtLikes
from exception_handlers.post import PostNotFound, UserNotFound
from exception_handlers.comment import CommentNotFound
from comment.models.comment import Comment
from post.api.serializers import PostLikeSerializerMany
from post.models.like import Like
from post.models.post import Post
from user_profile.models import User


class LikePostAPIViewGet(APIView):
    serializer_class = PostLikeSerializerMany

    def get(self, request: Request, post_id: int) -> Response:
        content_type = ContentType.objects.get_for_model(Post)
        likes = Like.objects.filter(
            content_type=content_type, object_id=post_id
        ).values()
        return OkResponse({'post_likes': list(likes)})


class LikePostAPIViewPost(APIView):
    def post(self, request: Request, post_id: int) -> Response:
        if (user_id := request.user.id) is None:
            raise NotRequiredData
        if (user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        if (post := Post.objects.filter(id=post_id).first()) is None:
            raise PostNotFound(post_id)

        content_type = ContentType.objects.get_for_model(Post)

        like = Like(user=user, content_type=content_type, object_id=post.id)
        Like.objects.bulk_create([like], ignore_conflicts=True)
        return SuccessResponse()


class LikePostAPIViewDelete(APIView):
    def delete(self, request: Request, post_id: int) -> Response:
        if (user_id := request.user.id) is None:
            raise NotRequiredData

        sub = User.objects.filter(id=user_id)
        ctype = ContentType.objects.get_for_model(Post)
        Like.objects.filter(
            Q(user=sub) & Q(content_type=ctype) & Q(object_id=post_id)
        ).delete()
        return DeleteResponse()


class LikeCommentAPIView(APIView):
    def get(self, request: Request, post_id: int, comment_id: int) -> Response:
        content_type = ContentType.objects.get_for_model(Comment)
        likes = Like.objects.filter(
            content_type=content_type, object_id=comment_id
        ).values()
        return OkResponse({'comment_likes': list(likes)})

    def post(
        self, request: Request, post_id: int, comment_id: int
    ) -> Response:
        if (user_id := request.user.id) is None:
            raise NotRequiredData
        if (user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        if Post.objects.filter(id=post_id).first() is None:
            raise PostNotFound(post_id)
        if (comment := Comment.objects.filter(id=comment_id).first()) is None:
            raise CommentNotFound(comment_id)

        ctype = ContentType.objects.get_for_model(Comment)
        exist_like = Like.objects.filter(
            Q(user=user) & Q(content_type=ctype) & Q(object_id=comment.id)
        ).first()
        if exist_like:
            raise EnoughtLikes
        new_like = Like.objects.create(
            user=user, content_type=ctype, object_id=comment_id
        )
        return CreateResponse({'id': new_like.id})

    def delete(
        self, request: Request, post_id: int, comment_id: int
    ) -> Response:
        if (user_id := request.user.id) is None:
            raise NotRequiredData
        sub = User.objects.get(id=user_id)
        ctype = ContentType.objects.get_for_model(Comment)
        like = Like.objects.get(
            user=sub, content_type=ctype, object_id=comment_id)
        like.delete()
        return DeleteResponse()


class AllLikesForUserAPIView(APIView):
    def get(self, request: Request, user_id: int) -> Response:
        if (user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        content_type = ContentType.objects.get_for_model(Post)
        post_likes = Like.objects.filter(
            content_type=content_type, user=user
        ).values()
        content_type = ContentType.objects.get_for_model(Comment)
        comment_likes = Like.objects.filter(
            content_type=content_type, user=user
        ).values()
        return OkResponse(
            {
                'post_likes': list(post_likes),
                'comment_likes': list(comment_likes)
            }
        )


class AllMyLikesAPIView(AllLikesForUserAPIView):
    def get(self, request: Request) -> Response:
        return super().get(request, request.user.id)
