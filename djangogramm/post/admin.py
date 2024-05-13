from django.contrib import admin

from post.models.like import Like
from comment.models.comment import Comment

admin.site.register(Like)
admin.site.register(Comment)
