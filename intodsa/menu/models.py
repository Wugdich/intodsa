from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=20)
    url = models.URLField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
