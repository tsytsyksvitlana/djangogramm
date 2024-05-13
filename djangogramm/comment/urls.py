from django.urls import path

from comment.sites.views import (
    AddCommentView, EditCommentView, DeleteCommentView, CommentLikeView
)
from comment.api.views import (
    CommentAPIView, CommentByIdAPIView, AllCommentsForUserAPIView,
    AllMyCommentsAPIView
)


urlpatterns = [
    path(
        'post/<int:post_id>/add_comment',
        AddCommentView.as_view(),
        name='add_comment'
    ),
    path(
        'post/<int:post_id>/comment/<int:pk>/edit',
        EditCommentView.as_view(),
        name='edit_comment'
    ),
    path(
        'post/<int:post_id>/comment/<int:pk>/delete/',
        DeleteCommentView.as_view(),
        name='delete_comment'
    ),
    path(
        'comment/<int:comment_id>/like',
        CommentLikeView.as_view(),
        name='comment_like'
    ),

    path('api/v1/post/<int:post_id>/comment', CommentAPIView.as_view()),
    path(
        'api/v1/post/<int:post_id>/comment/<int:comment_id>',
        CommentByIdAPIView.as_view()
    ),
    path(
        'api/v1/user/<int:user_id>/comment',
        AllCommentsForUserAPIView.as_view()
    ),
    path('api/v1/my/comment', AllMyCommentsAPIView.as_view())
]
