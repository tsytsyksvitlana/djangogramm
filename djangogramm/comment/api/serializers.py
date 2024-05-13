from rest_framework.utils.serializer_helpers import ReturnDict

from rest_framework import serializers

from comment.models.comment import Comment
from post.models.like import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'time_creation']


class CommentSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(read_only=True)
    count_likes = serializers.SerializerMethodField(read_only=True)
    user = serializers.SlugRelatedField(
        read_only=True, many=False, slug_field='username'
    )

    post = serializers.SerializerMethodField()

    likes = serializers.SerializerMethodField()
    count_likes = serializers.ReadOnlyField(source='likes.count')
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'text',
            'user',
            'time_creation',
            'is_liked',
            'count_likes',
            'likes'
        ]

    def get_post(self, obj: Comment) -> int:
        return obj.post.id

    def get_likes(self, obj: Comment) -> ReturnDict:
        _serializer = LikeSerializer(instance=obj.likes, many=True)
        return _serializer.data

    def get_is_liked(self, obj: Comment) -> bool:
        user = self.context['request'].user
        return obj.likes.filter(user=user).exists()
