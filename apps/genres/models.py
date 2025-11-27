from django.db import models

from apps.core.models import BaseModel


class Genre(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
