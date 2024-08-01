from django.urls import path

from user_profile.sites.views import (
    EditProfileView, SelfProfileView, SomeoneProfileView, UserFollowView
)
from user_profile.api.views import (
    FollowerAPIView, FollowerByIdAPIView, FollowingAPIView,
    FollowingByIdAPIView, UserProfileAPIView, MyProfileAPIView, MyAvatarAPIView
)


urlpatterns = [
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/me/', SelfProfileView.as_view(), name='self_profile'),
    path(
        'profile/<int:pk>/',
        SomeoneProfileView.as_view(),
        name='other_profile'
    ),
    path(
        'profile/<int:user_id>/follow',
        UserFollowView.as_view(),
        name='user_follow'
    ),

    path('api/v1/user/<int:user_id>/follower', FollowerAPIView.as_view()),
    path(
        'api/v1/user/<int:user_id>/follower/<int:follower_id>',
        FollowerByIdAPIView.as_view()
    ),
    path('api/v1/user/<int:user_id>/following', FollowingAPIView.as_view()),
    path(
        'api/v1/user/<int:user_id>/following/<int:following_id>',
        FollowingByIdAPIView.as_view()
    ),
    path('api/v1/user/<int:user_id>/profile', UserProfileAPIView.as_view()),
    path('api/v1/my/profile', MyProfileAPIView.as_view()),
    path('api/v1/my/avatar', MyAvatarAPIView.as_view())
]
