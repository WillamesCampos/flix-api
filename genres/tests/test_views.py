import pytest
from django.urls import reverse
from rest_framework import status
from app.tests import BaseAPITest
from genres.models import Genre
from genres.tests.factories import GenreFactory


@pytest.fixture
def genre_data():
    return {
        'name': 'Action'
    }

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

        data = {
            "name": ""
        }

        url = reverse('genre-create-list')
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
        assert 'This field may not be blank.' in response.data['name']

    def test_create_genre_invalid_name_as_number(self):
        self.give_permissions(model=Genre)

        data = {
            "name": 12345
        }

        url = reverse('genre-create-list')
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
        assert 'A valid string is required.' in response.data['name']
        assert Genre.objects.count() == 0

    def test_create_genre_name_too_long(self):
        self.give_permissions(model=Genre)

        data = {
            "name": "A" * 256  # Assuming max length is 255
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
        assert response.status_code == status.HTTP_403_FORBIDDEN, (
            "Esperado 403 para usuário sem permissão de acesso."
        )

    def test_create_genre_user_not_authenticated(self, genre_data):
        self.client.logout()
        data = genre_data
        url = reverse('genre-create-list')

        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f"Esperado 401 para usuário não autenticado, retornou {response.status_code}"
        )