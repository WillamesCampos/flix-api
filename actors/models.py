from django.db import models

from core.models import BaseModel

NATIONALITY_CHOICES = (
    # (valor armazenado, valor exibido)
    ('USA', 'United States of America'),
    ('BRA', 'Brazil'),
)


class Actor(BaseModel):
    name = models.CharField(max_length=200)
    birthday = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, choices=NATIONALITY_CHOICES, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
