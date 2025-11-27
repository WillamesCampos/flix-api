import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from app.tests import BaseAPITest
from apps.genres.models import Genre
from apps.genres.tests.factories import GenreFactory


@pytest.fixture
def genre_data():
    return {'name': 'Action'}


@pytest.fixture
def existing_genre():
    return GenreFactory(name='Drama')


@pytest.mark.django_db
class TestGenreAPI(BaseAPITest):
    def test_create_genre_success(self, genre_data):
        self.give_permissions(model=Genre)

        data = genre_data
        url = reverse('genre-create-list')

        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Genre.objects.count() == 1
        assert Genre.objects.get().name == genre_data['name']

    def test_create_genre_invalid_data_empty_name(self):
        self.give_permissions(model=Genre)

        data = {'name': ''}

        url = reverse('genre-create-list')
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
        assert 'This field may not be blank.' in response.data['name']

    def test_create_genre_invalid_name_as_number(self):
        self.give_permissions(model=Genre)

        data = {'name': 12345}

        url = reverse('genre-create-list')
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
        assert 'A valid string is required.' in response.data['name']
        assert Genre.objects.count() == 0

    def test_create_genre_name_too_long(self):
        self.give_permissions(model=Genre)

        data = {
            'name': 'A' * 256  # Assuming max length is 255
        }

        url = reverse('genre-create-list')
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
        assert 'Ensure this field has no more than 200 characters.' in response.data['name']

    def test_create_genre_without_permissions(self, genre_data):
        data = genre_data

        url = reverse('genre-create-list')
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Esperado 403 para usuário sem permissão de acesso.'

    def test_create_genre_user_not_authenticated(self, genre_data):
        self.client.logout()
        data = genre_data
        url = reverse('genre-create-list')

        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f'Esperado 401 para usuário não autenticado, retornou {response.status_code}'

    def test_list_genres(self, existing_genre):
        self.give_permissions(model=Genre)

        GenreFactory.create_batch(5)

        url = reverse('genre-create-list')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == Genre.objects.count()

    def test_list_genres_without_permissions(self, existing_genre):
        url = reverse('genre-create-list')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Esperado 403 para usuário sem permissão de acesso.'

    def test_list_genres_user_not_authenticated(self, existing_genre):
        self.client.logout()
        url = reverse('genre-create-list')

        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f'Esperado 401 para usuário não autenticado, retornou {response.status_code}'

    def test_retrieve_genre(self, existing_genre):
        self.give_permissions(model=Genre)

        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == existing_genre.name

    def test_retrieve_genre_not_found(self):
        self.give_permissions(model=Genre)

        url = reverse('genre-detail-view', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_genre_without_permissions(self, existing_genre):
        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Esperado 403 para usuário sem permissão de acesso.'

    def test_retrieve_genre_user_not_authenticated(self, existing_genre):
        self.client.logout()
        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})

        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f'Esperado 401 para usuário não autenticado, retornou {response.status_code}'

    def test_update_genre(self, existing_genre):
        self.give_permissions(model=Genre)

        updated_data = {'name': 'Updated Genre'}
        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})

        response = self.client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        existing_genre.refresh_from_db()
        assert existing_genre.name == updated_data['name']

    def test_update_genre_invalid_data(self, existing_genre):
        self.give_permissions(model=Genre)

        updated_data = {'name': ''}
        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})

        response = self.client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
        assert 'This field may not be blank.' in response.data['name']

    def test_update_genre_without_permissions(self, existing_genre):
        updated_data = {'name': 'Updated Genre'}
        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})

        response = self.client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Esperado 403 para usuário sem permissão de acesso.'

    def test_update_genre_user_not_authenticated(self, existing_genre):
        self.client.logout()
        updated_data = {'name': 'Updated Genre'}
        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})

        response = self.client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f'Esperado 401 para usuário não autenticado, retornou {response.status_code}'

    def test_delete_genre(self, existing_genre):
        self.give_permissions(model=Genre)

        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})
        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Genre.objects.filter(pk=existing_genre.pk).exists()

    def test_delete_genre_not_found(self):
        self.give_permissions(model=Genre)

        url = reverse('genre-detail-view', kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_genre_without_permissions(self, existing_genre):
        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})
        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN, 'Esperado 403 para usuário sem permissão de acesso.'

    def test_delete_genre_user_not_authenticated(self, existing_genre):
        self.client.logout()
        url = reverse('genre-detail-view', kwargs={'pk': existing_genre.pk})

        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f'Esperado 401 para usuário não autenticado, \
            retornou {response.status_code}'
        )


@pytest.mark.django_db
class TestGenreBulkCreateAPI(BaseAPITest):
    EXPECTED_CREATED_FIVE = 5
    EXPECTED_CREATED_TWO = 2
    EXPECTED_SKIPPED_TWO = 2
    EXPECTED_SKIPPED_THREE = 3
    EXPECTED_SKIPPED_ZERO = 0

    def test_bulk_create_genres_success(self):
        self.give_permissions(model=Genre)

        data = {'genres': ['Ação', 'Comédia', 'Drama', 'Terror', 'Suspense']}
        url = reverse('genre-bulk-create')

        initial_count = Genre.objects.count()
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['created'] == self.EXPECTED_CREATED_FIVE
        assert response.data['skipped'] == self.EXPECTED_SKIPPED_ZERO
        assert len(response.data['created_genres']) == self.EXPECTED_CREATED_FIVE
        assert len(response.data['skipped_genres']) == self.EXPECTED_SKIPPED_ZERO
        assert Genre.objects.count() == initial_count + self.EXPECTED_CREATED_FIVE

    def test_bulk_create_genres_skip_existing(self):
        self.give_permissions(model=Genre)

        GenreFactory(name='Ação')
        GenreFactory(name='Comédia')

        data = {'genres': ['Ação', 'Comédia', 'Drama', 'Terror']}
        url = reverse('genre-bulk-create')

        initial_count = Genre.objects.count()
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['created'] == self.EXPECTED_CREATED_TWO
        assert response.data['skipped'] == self.EXPECTED_SKIPPED_TWO
        assert len(response.data['created_genres']) == self.EXPECTED_CREATED_TWO
        assert len(response.data['skipped_genres']) == self.EXPECTED_SKIPPED_TWO
        assert 'Ação' in response.data['skipped_genres']
        assert 'Comédia' in response.data['skipped_genres']
        assert Genre.objects.count() == initial_count + self.EXPECTED_CREATED_TWO

    def test_bulk_create_genres_all_existing(self):
        self.give_permissions(model=Genre)

        GenreFactory(name='Ação')
        GenreFactory(name='Comédia')
        GenreFactory(name='Drama')

        data = {'genres': ['Ação', 'Comédia', 'Drama']}
        url = reverse('genre-bulk-create')

        initial_count = Genre.objects.count()
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['created'] == self.EXPECTED_SKIPPED_ZERO
        assert response.data['skipped'] == self.EXPECTED_SKIPPED_THREE
        assert len(response.data['created_genres']) == self.EXPECTED_SKIPPED_ZERO
        assert len(response.data['skipped_genres']) == self.EXPECTED_SKIPPED_THREE
        assert Genre.objects.count() == initial_count

    def test_bulk_create_genres_case_insensitive(self):
        EXPECTED_SKIPPED = 1
        self.give_permissions(model=Genre)

        GenreFactory(name='ação')

        data = {'genres': ['Ação', 'COMÉDIA', 'drama']}
        url = reverse('genre-bulk-create')

        initial_count = Genre.objects.count()
        response = self.client.post(url, data, format='json')

        genres_created = Genre.objects.filter(name__in=data['genres'])

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['created'] == genres_created.count()
        assert response.data['skipped'] == EXPECTED_SKIPPED
        assert 'Ação' in response.data['skipped_genres']
        assert Genre.objects.count() == initial_count + genres_created.count()

    def test_bulk_create_genres_remove_duplicates_in_list(self):
        self.give_permissions(model=Genre)

        data = {'genres': ['Ação', 'ação', 'AÇÃO', 'Comédia', 'comédia']}
        url = reverse('genre-bulk-create')

        initial_count = Genre.objects.count()
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        genres_created = Genre.objects.filter(name__in=data['genres'])
        assert response.data['created'] == genres_created.count()
        assert Genre.objects.count() == initial_count + genres_created.count()

    def test_bulk_create_genres_empty_list(self):
        self.give_permissions(model=Genre)

        data = {'genres': []}
        url = reverse('genre-bulk-create')

        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'genres' in response.data

    def test_bulk_create_genres_invalid_numeric_name(self):
        self.give_permissions(model=Genre)

        data = {'genres': ['Ação', '12345', 'Comédia']}
        url = reverse('genre-bulk-create')

        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'genres' in response.data

    def test_bulk_create_genres_without_permissions(self):
        data = {'genres': ['Ação', 'Comédia']}
        url = reverse('genre-bulk-create')

        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_bulk_create_genres_user_not_authenticated(self):
        self.client.logout()
        data = {'genres': ['Ação', 'Comédia']}
        url = reverse('genre-bulk-create')

        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_bulk_create_genres_response_structure(self):
        self.give_permissions(model=Genre)

        GenreFactory(name='Ação')

        data = {'genres': ['Ação', 'Comédia', 'Drama']}
        url = reverse('genre-bulk-create')

        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'created' in response.data
        assert 'skipped' in response.data
        assert 'created_genres' in response.data
        assert 'skipped_genres' in response.data
        assert isinstance(response.data['created'], int)
        assert isinstance(response.data['skipped'], int)
        assert isinstance(response.data['created_genres'], list)
        assert isinstance(response.data['skipped_genres'], list)

        if response.data['created_genres']:
            created_genre = response.data['created_genres'][0]
            assert 'uuid' in created_genre
            assert 'name' in created_genre
            assert 'created_at' in created_genre
            assert 'updated_at' in created_genre
