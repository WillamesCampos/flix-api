from datetime import date

import pytest

from actors.serializers import ActorSerializer
from movies.serializers import MovieListDetailSerializer
from movies.tests.factories import MovieFactory


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

        assert validated['id'] == movie.uuid
        assert validated['title'] == movie.title
        assert validated['genre']['id'] == movie.genre.uuid
        assert validated['release_date'] == movie.release_date.strftime('%Y-%m-%d')
        assert validated['resume'] == movie.resume
        assert isinstance(validated['actors'], list)

        actors = list(map(lambda actor: ActorSerializer(actor).data, movie.actors.all()))
        assert validated['actors'] == actors
