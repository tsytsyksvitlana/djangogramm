from django.urls import path

from post.api.views.post import (
    AllMyPostsAPIView,
    AllPostsForUserAPIView,
    PostAPIView,
    PostByIdAPIView
)
from post.api.views.like import (
    AllLikesForUserAPIView,
    AllMyLikesAPIView,
    LikeCommentAPIView,
    LikePostAPIViewGet,
    LikePostAPIViewPost,
    LikePostAPIViewDelete,
)
from post.sites.views import (
    AddPostView,
    DeletePostView,
    EditPostView,
    FeedView,
    HomeView,
    PostDetail,
    PostLikeView
)

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('feed/', FeedView.as_view(), name='feed'),

    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('post/edit/<int:pk>', EditPostView.as_view(), name='edit_post'),
    path('post/delete/<int:pk>', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:post_id>/like', PostLikeView.as_view(), name='post_like'),

    path(PostAPIView.url, PostAPIView.as_view()),
    path('api/v1/post/<int:post_id>', PostByIdAPIView.as_view()),
    path('api/v1/post/<int:post_id>/like', LikePostAPIViewGet.as_view()),
    path('api/v1/post/<int:post_id>/like', LikePostAPIViewPost.as_view()),
    path('api/v1/post/<int:post_id>/like', LikePostAPIViewDelete.as_view()),

    path(
        'api/v1/post/<int:post_id>/comment/<int:comment_id>/like',
        LikeCommentAPIView.as_view()
    ),
    path('api/v1/user/<int:user_id>/post', AllPostsForUserAPIView.as_view()),
    path('api/v1/my/post', AllMyPostsAPIView.as_view()),
    path(
        'api/v1/user/<int:user_id>/like', AllLikesForUserAPIView.as_view()
    ),
    path('api/v1/my/like', AllMyLikesAPIView.as_view())
]
