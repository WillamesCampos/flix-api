import pytest

from django.db import DataError, IntegrityError

from genres.tests.factories import GenreFactory
from genres.models import Genre

@pytest.mark.django_db
class TestModelGenre:

    def test_create_genre(self):
        genre = GenreFactory()
        assert isinstance(genre, Genre)
        assert genre.name is not None

    def test_genre_str(self):
        genre = GenreFactory(name='Action')
        assert str(genre) == 'Action'

        assert Genre.objects.count() == 1

    def test_genre_name_max_length(self):
        long_name = 'A' * 201
        with pytest.raises(DataError):
            Genre.objects.create(name=long_name)

    def test_genre_without_name(self):
        with pytest.raises(IntegrityError):
            Genre.objects.create(name=None)
