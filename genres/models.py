from django.db import models

from core.models import BaseModel


class Genre(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
