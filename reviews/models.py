from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import BaseModel
from movies.models import Movie


class Review(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='reviews')
    stars = models.IntegerField(
        # Model validators
        validators=[
            MinValueValidator(limit_value=0, message="The review can't be less than 0 stars."),
            MaxValueValidator(limit_value=5, message="The review can't be more than 5 stars."),
        ]
    )
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.movie} - {self.stars} stars'
