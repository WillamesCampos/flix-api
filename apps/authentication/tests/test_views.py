from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.tests.factories import UserFactory


@pytest.fixture
def url_token():
    return reverse('token_obtain_pair')


@pytest.fixture
def url_refresh_token():
    return reverse('token_refresh')


@pytest.fixture
def url_verify_token():
    return reverse('token_verify')


@pytest.fixture
def user_password():
    return 'AKnownP@ssword!_'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(user_password):
    return UserFactory(password=user_password)


@pytest.mark.django_db
class TestAuthenticationAPI:
    def test_user_authentication_success(self, url_token, user_password, client, user):
        user_obj = {'username': user.username, 'password': user_password}

        url = url_token
        response = client.post(url, user_obj)

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_user_authentication_failed(self, url_token, client, user):
        user_obj = {'username': user.username, 'password': 'UnknownP@ssword!'}

        response = client.post(url_token, user_obj)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'No active account found with the given credentials' == str(response.data['detail'])

    def test_token_refresh_success(self, url_token, url_refresh_token, client, user, user_password):
        login_data = {'username': user.username, 'password': user_password}
        login_response = client.post(url_token, login_data)

        assert login_response.status_code == status.HTTP_200_OK

        refresh_data = {'refresh': login_response.data['refresh']}

        refresh_response = client.post(url_refresh_token, refresh_data)

        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data
        assert refresh_response.data['access'] is not None

    def test_token_refresh_with_expired_refresh_token(self, url_refresh_token, client, user):
        refresh = RefreshToken.for_user(user)

        refresh.set_exp(lifetime=timedelta(seconds=-1))

        refresh_data = {'refresh': str(refresh)}

        response = client.post(url_refresh_token, refresh_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_with_expired_token(self, url_token, url_verify_token, client, user, user_password):
        login_data = {'username': user.username, 'password': user_password}
        login_response = client.post(url_token, login_data)

        assert login_response.status_code == status.HTTP_200_OK

        verify_data = {'token': login_response.data['access']}

        verify_response = client.post(url_verify_token, verify_data)
        assert verify_response.status_code == status.HTTP_200_OK
