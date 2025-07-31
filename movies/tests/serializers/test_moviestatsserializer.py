import pytest

from movies.serializers import MovieStatsSerializer
from movies.tests.factories import MovieFactory
from reviews.tests.factories import ReviewFactory


@pytest.fixture
def movie_factory():
    return MovieFactory()


@pytest.mark.django_db
class TestMovieStatsSerializer:
    def setup_method(self):
        self.serializer = MovieStatsSerializer

    def test_movie_stats_serializer_fields(self):
        fields = self.serializer().fields
        assert 'total_movies' in fields
        assert 'movies_by_genre' in fields
        assert 'total_reviews' in fields
        assert 'average_stars' in fields

    def test_movie_stats_serializer_valid_data(self, list_review_factory):
        movies = MovieFactory.create_batch(3)
        for index, movie in enumerate(movies):
            movie.reviews.set(list_review_factory[index])

        data = {
            'total_movies': len(movies),
            'movies_by_genre': [{'genre__name': movie.genre.name, 'count': 1} for movie in movies],
            'total_reviews': sum(len(movie.reviews.all()) for movie in movies),
            'average_stars': sum(review.stars for review in ReviewFactory.create_batch(5)) / 5,
        }

        serializer = self.serializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data
