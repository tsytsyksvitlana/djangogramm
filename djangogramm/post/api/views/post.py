import typing as t

from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    Count,
    Exists,
    Prefetch,
    QuerySet
)
from django.db.models.manager import BaseManager

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.responses.success import (
    OkResponse,
    CreateResponse,
    DeleteResponse
)
from exception_handlers.base import NotRequiredData, NoAuthUser
from exception_handlers.post import PostNotFound, UserNotFound
from comment.models.comment import Comment
from post.api.serializers import PostSerializer
from post.models.image import Image
from post.models.like import Like
from post.models.post import Post
from post.models.tag import Tag
from user_profile.models import User


class PostBaseAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    serializer_class = PostSerializer

    def get_queryset(self) -> BaseManager[Post]:
        user = t.cast(User, self.request.user)

        like_comment = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Comment),
        )
        like_post = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Post)
        )
        like_comment_prefetch = Prefetch(
            'likes',
            queryset=like_comment,
        )
        post_likes = Prefetch('likes', queryset=like_post)

        if not user.is_anonymous:
            like_comment = like_comment.filter(user=user)
            like_post = like_post.filter(user=user)

        post_comment = Prefetch(
            'comments',
            queryset=Comment.objects.prefetch_related(like_comment_prefetch)
            .select_related('user')
            .annotate(count_likes=Count('likes'), is_liked=Exists(like_post))
        )
        post_images = Prefetch(
            'images',
            queryset=Image.objects.all(),
        )

        posts = Post.objects.prefetch_related(
            post_likes, post_comment, post_images, 'tags', 'user'
        ).annotate(
            count_likes=Count('likes'),
            api_is_liked=Exists(like_post),
        )
        return posts

    def get(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        return self.list(request, *args, **kwargs)

    def post(
            self, request: Request, *args: t.Any, **kwargs: t.Any
    ) -> Response:
        return self.create(request, *args, **kwargs)


class PostViewPost(PostBaseAPIView):
    def get_queryset(self) -> QuerySet[Post]:
        queryset = super().get_queryset().filter(id=self.kwargs['post_id'])
        return queryset


class PostAPIView(PostBaseAPIView):
    serializer_class = PostSerializer
    url: t.Literal['api/v1/post/'] = 'api/v1/post/'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        serialize = self.get_serializer(self.get_queryset(), many=True)
        return OkResponse(serialize.data)

    def post(self, request: Request) -> Response:
        description = request.get('description')
        current_user = request.user.id

        if description is None or current_user is None:
            raise NotRequiredData

        if not isinstance(description, str):
            raise NotRequiredData

        if (user := User.objects.filter(id=current_user).first()) is None:
            raise UserNotFound(current_user)

        new_post = Post.objects.create(description=description, user=user)
        return CreateResponse({'id': new_post.id})


class PostByIdAPIView(PostBaseAPIView):
    serializer_class = PostSerializer

    def get_object(self, request: Request, post_id: int) -> Post:
        if (user := request.user) is None:
            raise NotRequiredData
        if (
            post := super().get_queryset().filter(pk=post_id, user=user).first()
        ) is None:
            raise PostNotFound(post_id)
        return post

    def get(self, request: Request, post_id: int) -> Response:
        qs = self.get_queryset().filter(pk=post_id)
        if not qs.exists():
            raise PostNotFound(post_id)
        return OkResponse(self.get_serializer(qs, many=True).data)

    def put(self, request: Request, post_id: int) -> Response:
        post = self.get_object(request, post_id)
        serializer = PostSerializer(
            post, data=request.data, partial=True, context={'request': request}
        )
        if not serializer.is_valid():
            raise NotRequiredData
        serializer.save()
        tags = request.data.get('tags')
        if tags is not None:
            post.tags.clear()
            for tag in tags:
                tag_instance, _ = Tag.objects.get_or_create(tag=tag)
                post.tags.add(tag_instance)
        post.save()
        return CreateResponse(serializer.data)

    def delete(self, request: Request, post_id: int) -> Response:
        self.get_object(request, post_id).delete()
        return DeleteResponse()


class AllPostsForUserAPIView(PostAPIView):
    def get(self, request: Request, user_id: int) -> Response:
        if (user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        qs = self.get_queryset().filter(user=user)
        serialize = self.get_serializer(qs, many=True)
        return OkResponse(serialize.data)


class AllMyPostsAPIView(AllPostsForUserAPIView):
    def get(self, request: Request) -> Response:
        return super().get(request, request.user.id)
