from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=20)
    # 'path' is MenuItem unique identifier
    path = models.CharField(max_length=200)
    parent = models.ForeignKey(
            'self',
            on_delete=models.CASCADE,
            null=True,
            blank=True,
            )

    def __str__(self):
        return self.title
