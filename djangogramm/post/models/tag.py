from django.db import models


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(
        max_length=20, unique=True, null=False, blank=False
    )

    def __str__(self):
        return f'Tag(id={self.id}, tag={self.tag})'
