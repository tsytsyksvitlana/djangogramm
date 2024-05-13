from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user_profile.User', on_delete=models.CASCADE)
    time_creation = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        return f'Like(user = {self.user}, {self.time_creation})'
