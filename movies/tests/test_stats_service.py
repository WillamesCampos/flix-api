import pytest
from django.db.models import QuerySet

from movies.models import Movie
from movies.services.stats_service import stats_service
from movies.tests.factories import MovieFactory


@pytest.mark.django_db
class TestStatsService:
    def setup_method(self):
        self.service = stats_service

    def test_build_data(self, list_review_factory):
        movies = MovieFactory.create_batch(3)
        movies_ids = []
        for index, movie in enumerate(movies):
            movie.reviews.set(list_review_factory[index])
            movies_ids.append(movie.uuid)

        service = self.service(queryset=Movie.objects.filter(uuid__in=movies_ids))
        data = service.build_data()

        assert data['total_movies'] == len(movies)
        assert len(data['movies_by_genre']) == len(set(movie.genre.name for movie in movies))
        assert data['total_reviews'] == sum(len(movie.reviews.all()) for movie in movies)
        assert isinstance(data['average_stars'], float)

    def test_build_data_empty_queryset(self):
        queryset = QuerySet(model=Movie)
        service = self.service(queryset=queryset.none())
        data = service.build_data()

        assert data['total_movies'] == 0
        assert not data['movies_by_genre']
        assert data['total_reviews'] == 0
        assert data['average_stars'] == 0.0
