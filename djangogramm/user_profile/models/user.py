from django.contrib.auth.models import AbstractUser
from django.db import models

from user_profile.models.follower import Follower


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField()
    avatar = models.ImageField(
        upload_to='avatars/', null=True
    )

    password = models.CharField(max_length=20, db_column='password')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'User(id={self.id}, username={self.username})'

    @property
    def get_followers_count(self):
        return Follower.objects.filter(following=self).count()

    @property
    def get_following_count(self):
        return Follower.objects.filter(follower=self).count()

    @property
    def is_followed(self):
        return Follower.objects.filter(following=self).exists()
