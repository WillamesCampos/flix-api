import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from app.tests import BaseAPITest
from movies.models import Movie
from movies.tests.factories import MovieFactory


@pytest.fixture
def movie_data(genre_factory, list_of_actors_id_factory):
    return {
        'title': 'Inception',
        'genre': genre_factory.uuid,
        'release_date': '2010-07-16',
        'actors': list_of_actors_id_factory,
        'resume': 'A thief who steals corporate secrets through the use \
            of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.',
    }


@pytest.fixture
def existing_movie():
    return MovieFactory()


@pytest.mark.django_db
class TestMoviesAPI(BaseAPITest):
    def test_list_movies_success(self):
        self.give_permissions(model=Movie)

        MovieFactory.create_batch(5)

        url = reverse('movie-create-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK, f'Expected 200 OK, got {response.status_code}'
        assert isinstance(response.data, list), 'Response data should be a list of movies'
        assert len(response.data) == Movie.objects.count(), (
            'Response data length should match the number of movies \
        in the database'
        )

    def test_list_movies_without_permissions(self):
        url = reverse('movie-create-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Expected 403 Forbidden for user without access permission.'

    def test_list_movies_user_not_authenticated(self):
        self.client.logout()
        url = reverse('movie-create-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f'Expected 401 Unauthorized for unauthenticated user, got {response.status_code}'

    def test_create_movie_success(self, movie_data):
        self.give_permissions(model=Movie)

        url = reverse('movie-create-list')
        response = self.client.post(url, movie_data)

        assert response.status_code == status.HTTP_201_CREATED, f'Expected 201 Created, got {response.status_code}'
        assert Movie.objects.filter(title=movie_data['title']).exists(), 'Movie should be created in the database'
        assert response.data['title'] == movie_data['title'], 'Response data should match the created movie data'

    def test_create_movie_without_permissions(self, movie_data):
        url = reverse('movie-create-list')
        response = self.client.post(url, movie_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Expected 403 Forbidden for user without access permission.'

    def test_create_movie_user_not_authenticated(self, movie_data):
        self.client.logout()
        self.give_permissions(model=Movie)

        url = reverse('movie-create-list')
        response = self.client.post(url, movie_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f'Expected 401 Unauthorized for unauthenticated user, got {response.status_code}'
        assert not Movie.objects.filter(title=movie_data['title']).exists(), 'Movie should not be created in the database'

    def test_retrieve_movie_success(self, existing_movie):
        self.give_permissions(model=Movie)

        movie = existing_movie
        url = reverse('movie-detail-view', kwargs={'pk': movie.uuid})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK, f'Expected 200 OK, got {response.status_code}'
        assert response.data['title'] == existing_movie.title, 'Response data should match the retrieved movie data'

    def test_retrieve_movie_not_found(self):
        self.give_permissions(model=Movie)

        url = reverse('movie-detail-view', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, f'Expected 404 Not Found, got {response.status_code}'

    def test_update_movie_success(self, existing_movie):
        self.give_permissions(model=Movie)

        movie = existing_movie
        updated_data = {'title': 'Updated Title'}

        url = reverse('movie-detail-view', kwargs={'pk': movie.uuid})
        response = self.client.patch(url, updated_data)

        movie.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK, f'Expected 200 OK, got {response.status_code}'
        assert movie.title == updated_data['title'], 'Movie title should be updated in the database'

    def test_update_movie_not_found(self):
        self.give_permissions(model=Movie)

        url = reverse('movie-detail-view', kwargs={'pk': uuid.uuid4()})
        response = self.client.patch(url, {'title': 'Updated Title'})
        assert response.status_code == status.HTTP_404_NOT_FOUND, f'Expected 404 Not Found, got {response.status_code}'

    def test_update_movie_without_permissions(self, existing_movie):
        movie = existing_movie
        url = reverse('movie-detail-view', kwargs={'pk': movie.uuid})
        response = self.client.patch(url, {'title': 'Updated Title'})

        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Expected 403 Forbidden for user without access permission.'
        movie.refresh_from_db()
        assert movie.title == existing_movie.title, 'Movie title should not be updated in the database'

    def test_update_movie_user_not_authenticated(self, existing_movie):
        self.client.logout()
        self.give_permissions(model=Movie)

        data = {'title': 'Updated Title'}

        movie = existing_movie
        url = reverse('movie-detail-view', kwargs={'pk': movie.uuid})
        response = self.client.patch(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f'Expected 401 Unauthorized for unauthenticated user, got {response.status_code}'
        movie.refresh_from_db()
        assert movie.title == existing_movie.title, 'Movie title should not be updated in the database'

    def test_delete_movie_success(self, existing_movie):
        self.give_permissions(model=Movie)

        movie = existing_movie
        url = reverse('movie-detail-view', kwargs={'pk': movie.uuid})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, f'Expected 204 No Content, got {response.status_code}'
        assert not Movie.objects.filter(id=movie.uuid).exists(), 'Movie should be deleted from the database'

    def test_delete_movie_not_found(self):
        self.give_permissions(model=Movie)

        url = reverse('movie-detail-view', kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, f'Expected 404 Not Found, got {response.status_code}'

    def test_delete_movie_without_permissions(self, existing_movie):
        movie = existing_movie
        url = reverse('movie-detail-view', kwargs={'pk': movie.uuid})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Expected 403 Forbidden for user without access permission.'
        assert Movie.objects.filter(id=movie.uuid).exists(), 'Movie should not be deleted from the database'

    def test_delete_movie_user_not_authenticated(self, existing_movie):
        self.client.logout()
        movie = existing_movie
        url = reverse('movie-detail-view', kwargs={'pk': movie.uuid})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f'Expected 401 Unauthorized for unauthenticated user, got {response.status_code}'
        assert Movie.objects.filter(id=movie.uuid).exists(), 'Movie should not be deleted from the database'


@pytest.mark.django_db
class TestMovieStatsAPI(BaseAPITest):
    def test_movie_stats_success(self):
        self.give_permissions(model=Movie)

        url = reverse('movie-stats-view')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK, f'Expected 200 OK, got {response.status_code}'
        assert 'total_movies' in response.data, 'Response data should contain total_movies'
        assert 'movies_by_genre' in response.data, 'Response data should contain movies_by_genre'
        assert 'total_reviews' in response.data, 'Response data should contain total_reviews'
        assert 'average_stars' in response.data, 'Response data should contain average_stars'

    def test_movie_stats_without_permissions(self):
        url = reverse('movie-stats-view')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Expected 403 Forbidden for user without access permission.'

    def test_movie_stats_user_not_authenticated(self):
        self.client.logout()
        url = reverse('movie-stats-view')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f'Expected 401 Unauthorized for unauthenticated user, got {response.status_code}'

    def test_movie_stats_empty_database(self):
        self.give_permissions(model=Movie)

        url = reverse('movie-stats-view')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK, f'Expected 200 OK, got {response.status_code}'
        assert response.data['total_movies'] == 0, 'Total movies should be 0 when no movies exist'
        assert not response.data['movies_by_genre'], 'Movies by genre should be empty when no movies exist'
        assert response.data['total_reviews'] == 0, 'Total reviews should be 0 when no movies exist'
        assert response.data['average_stars'] == 0.0, 'Average stars should be 0.0 when no movies exist'
