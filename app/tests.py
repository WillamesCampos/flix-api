import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.test_settings import faker_gen

User = get_user_model()


def user_obj():
    return {
        'username': faker_gen.user_name(),
        'email': faker_gen.email(),
        'password': faker_gen.password(length=8),
    }


@pytest.mark.django_db
class BaseAPITest:
    def setup_method(self):
        self.client = APIClient()
        self.user = None
        self.__password = ''
        self._user_permission_group = None

        self.user_data = user_obj()
        self.create_user(self.user_data)
        self.authenticate_user()

    def create_user(self, user_obj):
        self.__password = user_obj['password']

        self.user = User.objects.create_user(
            username=user_obj['username'],
            password=user_obj['password'],
            email=user_obj['email'],
        )

    def authenticate_user(self):
        url = reverse('token_obtain_pair')

        data = {'username': self.user.username, 'password': self.__password}

        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_200_OK, f'It has been not possible to create JWT token: {response.data}'

        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def __create_permission_group(self, name='TestAdminGroup'):
        self.__user_permission_group, _ = Group.objects.get_or_create(name=name)

    def give_permissions(self, model):
        self.__create_permission_group()

        app_label = model._meta.app_label
        model_name = model._meta.model_name

        permissions = Permission.objects.filter(content_type__app_label=app_label, content_type__model=model_name)

        self.__user_permission_group.permissions.add(*permissions)

        self.__user_permission_group.user_set.add(self.user)

        self.user.refresh_from_db()

    def revoke_permissions(self, group, user):
        user.groups.remove(group)
        user.refresh_from_db()
