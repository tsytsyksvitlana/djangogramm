from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Prefetch
from django.db.models.manager import BaseManager
from django.urls import reverse
from django.utils import timezone

from comment.models.comment import Comment
from post.models.image import Image


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    time_creation = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True)
    user = models.ForeignKey(
        'user_profile.User', related_name='posts', on_delete=models.CASCADE
    )
    likes = GenericRelation('post.Like', related_query_name='likes')
    tags = models.ManyToManyField('post.Tag', related_name='posts')

    def __str__(self) -> str:
        return f'Post(id={self.id}, user={self.user})'

    def get_absolute_url(self) -> str:
        return reverse('home')

    def view_is_liked(self, user) -> bool:
        return self.likes.filter(user=user).exists()

    @classmethod
    def _qs(cls) -> Prefetch:
        return Prefetch('post', queryset=cls.objects.all())

    @property
    def view_get_count_likes(self) -> int:
        return self.likes.count()

    @property
    def view_get_images_for_post(self) -> BaseManager[Image]:
        return (
            Image.objects.prefetch_related(self._qs())
            .filter(post=self)
            .all()
        )

    def get_images_for_post(self) -> BaseManager[Image]:
        return (
            Image.objects.prefetch_related(self._qs())
            .filter(post=self)
            .all()
        )

    @property
    def view_get_comments(self) -> BaseManager[Comment]:
        return (
            Comment.objects.prefetch_related(self._qs())
            .filter(post=self)
            .all()
        )
