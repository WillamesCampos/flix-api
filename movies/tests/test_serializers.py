import pytest

from movies.serializers import MovieModelSerializer


@pytest.fixture
def movie_data(genre_factory, list_of_actors_id_factory):
    return {
        'title': 'Inception',
        'genre': genre_factory.id,
        'release_date': '2010-07-16',
        'actors': list_of_actors_id_factory,
        'resume': 'A thief who steals corporate secrets through the use of dream-sharing technology \
        is given the inverse task of planting an idea into the mind of a CEO.',
    }


@pytest.mark.django_db
class TestMovieModelSerializer:
    def setup_method(self):
        self.serializer = MovieModelSerializer

    def test_movie_serializer_valid_data(self, movie_data):
        serializer = self.serializer(data=movie_data)

        assert serializer.is_valid()

        validated = serializer.validated_data

        assert movie_data['title'] == validated['title']
        assert movie_data['genre'] == validated['genre'].id
        assert movie_data['release_date'] == validated['release_date']
        assert movie_data['resume'] == validated['resume']
