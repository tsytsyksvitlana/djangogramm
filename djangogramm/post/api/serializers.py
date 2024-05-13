import typing as t
import logging

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from comment.api.serializers import CommentSerializer
from post.models import Post
from post.models.like import Like
from post.models.tag import Tag

log = logging.getLogger(__name__)

if t.TYPE_CHECKING:
    from django.db.models import QuerySet
    from post.models.image import Image
    from comment.models.comment import Comment


class PostImagesProtocol(t.Protocol):
    images: 'QuerySet[Image]'
    comments: 'QuerySet[Comment]'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'time_creation']


class PostLikeSerializerMany(serializers.Serializer):
    post_likes = LikeSerializer(many=True)

    def get_post_likes(self, obj: 'QuerySet[Like]') -> ReturnDict:
        return LikeSerializer(instance=obj, many=True).data


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='tag'
    )
    comments = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    count_likes = serializers.ReadOnlyField(source='likes.count')
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'images',
            'user',
            'time_creation',
            'description',
            'tags',
            'comments',
            'images',
            'likes',
            'count_likes',
            'is_liked'
        ]

    def get_user(self, obj: Post) -> str:
        return obj.user.username

    def get_comments(self, obj: PostImagesProtocol) -> ReturnDict:
        request = self.context.get('request')
        comment_serializer = CommentSerializer(
            instance=obj.comments.all(),
            many=True,
            context={'request': request}
        )
        return comment_serializer.data

    def get_images(self, obj: PostImagesProtocol) -> list[str]:
        return [image.image.url for image in obj.images.all()]

    def get_likes(self, obj: Post) -> ReturnDict:
        return LikeSerializer(instance=obj.likes, many=True).data

    # def get_is_liked(self, obj: PostImagesProtocol) -> bool:
    #     return obj.api_is_liked

    def get_is_liked(self, obj: Post) -> bool:
        return getattr(obj, 'api_is_liked')
