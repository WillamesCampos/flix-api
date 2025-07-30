import pytest
from django.db import DataError, IntegrityError

from movies.factories import MovieFactory
from movies.models import Movie


@pytest.mark.django_db
class TestModelMovie:
    def test_create_movie(self):
        movie = MovieFactory()

        assert isinstance(movie, Movie)
        assert movie.title is not None
        assert movie.genre is not None
        assert movie.release_date is not None
        assert movie.resume is not None
        assert movie.actors.count() == MovieFactory.DEFAULT_ACTORS_COUNT

    def test_movie_str(self):
        movie = MovieFactory(title='Inception')
        assert str(movie) == 'Inception'

        assert Movie.objects.count() == 1

    def test_movie_title_max_length(self, genre_factory):
        long_title = 'A' * 501
        with pytest.raises(DataError):
            Movie.objects.create(title=long_title, genre=genre_factory)

    def test_movie_without_title(self, genre_factory):
        with pytest.raises(IntegrityError):
            Movie.objects.create(title=None, genre=genre_factory)

    def test_movie_genre_protected_on_delete(self, genre_factory):
        genre = genre_factory
        MovieFactory(genre=genre_factory)

        with pytest.raises(IntegrityError):
            genre.delete()

    def test_movie_release_date_null(self):
        movie = MovieFactory(release_date=None)
        assert movie.release_date is None

    def test_movie_actors_related(self):
        movie = MovieFactory()
        assert movie.actors.count() == MovieFactory.DEFAULT_ACTORS_COUNT

        # Check if the actors are correctly linked to the movie
        for actor in movie.actors.all():
            assert movie in actor.movies.all()
