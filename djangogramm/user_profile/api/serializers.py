from rest_framework import serializers

from user_profile.models.user import User
from user_profile.models.follower import Follower


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'bio',
            'avatar', 'followers_count', 'following_count'
        ]
        read_only_fields = ['id', 'followers_count', 'following_count']
        extra_kwargs = {
            'first_name': {'required': False, 'allow_null': True},
            'last_name': {'required': False, 'allow_null': True},
            'bio': {'required': False, 'allow_null': True},
            'avatar': {'required': False, 'allow_null': True},
        }

    def get_followers_count(self, obj) -> int:
        return obj.get_followers_count

    def get_following_count(self, obj) -> int:
        return obj.get_following_count


class FollowerSerializer(serializers.ModelSerializer):
    follower_username = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ['follower_username']

    def get_follower_username(self, obj) -> list[str]:
        return [follower.username for follower in obj.follower.all()]


class FollowingSerializer(serializers.ModelSerializer):
    following_usernames = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ['following_usernames']

    def get_following_usernames(self, obj) -> list[str]:
        return [following.username for following in obj.following.all()]
