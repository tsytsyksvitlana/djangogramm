from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from user_profile.models.user import User


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_creation = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(
        'post.Post', on_delete=models.CASCADE, null=True, related_name='comments'
    )
    likes = GenericRelation('post.Like', related_query_name='likes')

    def __str__(self) -> str:
        return (f'Comment(id={self.id}, user={self.user}, post={self.post},'
                'time_creation={self.time_creation})')

    def view_is_liked(self, user):
        return self.likes.filter(user=user).exists()

    def is_liked(self, user):
        return self.likes.filter(user=user).exists()

    @property
    def view_get_count_likes(self):
        return self.likes.count()
