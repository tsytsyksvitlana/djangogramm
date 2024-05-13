from django.db import models


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(
        'post.Post', on_delete=models.CASCADE, blank=True, null=True,
        related_name='images'
    )

    def __str__(self):
        return f'Image(id={self.image_id})'
