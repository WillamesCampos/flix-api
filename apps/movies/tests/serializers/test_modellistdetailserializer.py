from datetime import date

import pytest

from apps.actors.serializers import ActorSerializer
from apps.movies.serializers import MovieListDetailSerializer
from apps.movies.tests.factories import MovieFactory


@pytest.fixture
def movie_factory():
    return MovieFactory()


@pytest.mark.django_db
class TestMovieListDetailSerializer:
    def setup_method(self):
        self.serializer = MovieListDetailSerializer

    def test_movie_list_detail_serializer_valid_data(self, movie_factory):
        movie = movie_factory
        movie.release_date = date(year=2010, month=7, day=16)
        serializer = self.serializer(instance=movie)

        validated = serializer.data

        assert validated['uuid'] == movie.uuid
        assert validated['title'] == movie.title
        assert validated['genre']['uuid'] == movie.genre.uuid
        assert validated['release_date'] == movie.release_date.strftime('%Y-%m-%d')
        assert validated['resume'] == movie.resume
        assert isinstance(validated['actors'], list)

        actors = list(map(lambda actor: ActorSerializer(actor).data, movie.actors.all()))
        assert validated['actors'] == actors
