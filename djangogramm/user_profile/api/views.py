import typing as t

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from utils.responses.success import (
    OkResponse,
    DeleteResponse,
    CreateResponse
)
from utils.responses.error import BadResponse
from exception_handlers.base import NotRequiredData
from exception_handlers.post import EnoughtFollowers, UserNotFound
from user_profile.api.serializers import (
    FollowerSerializer, FollowingSerializer, UserSerializer
)
from user_profile.models.follower import Follower
from user_profile.models.user import User


class FollowerAPIView(APIView):
    serializer_class = FollowerSerializer

    def get_queryset(self, user_id: int):
        if (user := User.objects.filter(id=user_id).first()) is None:
            return UserNotFound(user_id)
        return Follower.objects.filter(following=user).all()

    def get(self, request: Request, user_id: int) -> Response:
        followers = self.get_queryset(user_id)
        serialize = FollowerSerializer(followers, many=True)
        return OkResponse(serialize.data)

    def post(self, request: Request, user_id: int) -> Response:
        if (following_user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        if (id := request.data.get('user_id')) is None:
            raise NotRequiredData()
        if (follower_user := User.objects.filter(id=id).first()) is None:
            raise UserNotFound(id)
        if (
            Follower.objects
            .filter(follower=follower_user, following=following_user)
            .exists()
        ):
            raise EnoughtFollowers()
        follower = Follower.objects.create()
        follower.follower.add(follower_user)
        follower.following.add(following_user)
        return CreateResponse({'id': follower.id})


class FollowerByIdAPIView(FollowerAPIView):
    def delete(
        self, request: Request, user_id: int, follower_id: int
    ) -> Response:
        if (following_user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        if (follower_id != request.user.id):
            raise UserNotFound(user_id)
        if (follower_user := User.objects.filter(id=follower_id).first()) is None:
            raise UserNotFound(follower_id)
        follower = Follower.objects.get(
            follower=follower_user, following=following_user
        )
        follower.delete()
        return DeleteResponse()


class FollowingAPIView(APIView):
    def get(self, request: Request, user_id: int) -> Response:
        if (user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        followings = Follower.objects.filter(follower=user).all()
        serializer = FollowingSerializer(followings, many=True)
        return OkResponse(serializer.data)

    def post(self, request: Request, user_id: int) -> Response:
        if (follower_id := request.data.get('follower_id')) is None:
            raise NotRequiredData()
        if (follower_user := User.objects.get(id=follower_id)) is None:
            raise UserNotFound(follower_id)
        if (following_user := User.objects.get(id=user_id)) is None:
            raise UserNotFound(user_id)
        if (
            Follower.objects
            .filter(follower=follower_user, following=following_user)
            .exists()
        ):
            raise EnoughtFollowers()

        follower = Follower.objects.create()
        follower.follower.add(follower_user)
        follower.following.add(following_user)
        return CreateResponse({'id': follower.id})


class FollowingByIdAPIView(APIView):
    def delete(
        self, request: Request, user_id: int, following_id: int
    ) -> Response:
        if (following_user := User.objects.filter(id=following_id).first()) is None:
            raise UserNotFound(following_id)
        if (user_id != request.user.id):
            raise UserNotFound(user_id)
        if (follower_user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        follower = Follower.objects.get(
            follower=follower_user, following=following_user
        )
        follower.delete()
        return DeleteResponse()


class UserProfileAPIView(APIView):
    def get(self, request: Request, user_id: int) -> Response:
        if (user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        serializer = UserSerializer(user)
        return OkResponse(serializer.data)

    def put(self, request: Request, user_id: int) -> Response:
        if user_id != request.user.id:
            raise UserNotFound(user_id)
        if (user := User.objects.filter(id=user_id).first()) is None:
            raise UserNotFound(user_id)
        serializer = UserSerializer(user, data=request.data)
        if not serializer.is_valid():
            return BadResponse(serializer.errors)
        serializer.save()
        return OkResponse(serializer.data)


class MyProfileAPIView(APIView):
    def get(self, request: Request) -> Response:
        if (user := request.user) is None:
            raise NotRequiredData()
        if (user := User.objects.filter(id=user.id).first()) is None:
            raise UserNotFound(user.id)
        serializer = UserSerializer(user)
        return OkResponse(serializer.data)


class MyAvatarAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request: Request) -> Response:
        if (user := request.user) is None:
            raise NotRequiredData()
        if (user := User.objects.filter(id=user.id).first()) is None:
            raise UserNotFound(user.id)
        if not 'avatar' in request.FILES:
            raise NotRequiredData()
        user.avatar = request.FILES['avatar']
        user.save()
        return CreateResponse({'message': 'Avatar uploaded successfully'})

    def delete(self, request: Request) -> Response:
        if (user := request.user) is None:
            raise NotRequiredData
        if (user := User.objects.filter(id=user.id).first()) is None:
            raise UserNotFound(user.id)
        user.avatar.delete()
        user.avatar = None
        user.save()
        return DeleteResponse()
