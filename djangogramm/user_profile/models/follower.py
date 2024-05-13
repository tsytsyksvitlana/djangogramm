from django.db import models


class Follower(models.Model):
    follower = models.ManyToManyField(
        'user_profile.User', related_name='follower'
    )
    following = models.ManyToManyField(
        'user_profile.User', related_name='following'
    )

    def __str__(self):
        return f'{self.follower} is following {self.following}'
