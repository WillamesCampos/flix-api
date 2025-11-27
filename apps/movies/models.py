from django.db import models

from apps.actors.models import Actor
from apps.core.models import BaseModel
from apps.genres.models import Genre


class Movie(BaseModel):
    title = models.CharField(max_length=500)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,  # Se algum registro estiver associado a um gênero em uso, não vai permitir a deleção.
        related_name='movies',  # Facilita na queryset do Django ao usar .movies trazer todos os filmes que o Genre está ligado.
    )
    release_date = models.DateField(null=True, blank=True)
    actors = models.ManyToManyField(
        Actor,
        related_name='movies',  # Facilita na queryset do Django ao usar .movies trazer todos os filmes que o Actor está ligado.
    )
    resume = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
