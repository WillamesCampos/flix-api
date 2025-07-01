import pytest

from django.urls import reverse
from rest_framework import status

from app.test_settings import faker_gen
from app.tests import BaseAPITest
from .factories import ActorFactory

from actors.models import Actor
from actors.models import NATIONALITY_CHOICES


@pytest.fixture
def actor_data():
    return {
        'name': faker_gen.name_male(),
        'birthday': faker_gen.date_of_birth(),
        'nationality': faker_gen.random_choices(elements=[choice[0] for choice in NATIONALITY_CHOICES], length=1)
    }

@pytest.fixture
def existing_actor():
    return ActorFactory()


@pytest.mark.django_db
class TestActorAPI(BaseAPITest):

    def test_list_actors_success(self):
        size = 5
        ActorFactory.create_batch(size=size)
        self.give_permissions(model=Actor)

        url = reverse('actor-create-list')
        response = self.client.get(url)

        returned_names = {actor['name'] for actor in response.data}
        expected_names = set(Actor.objects.values_list('name', flat=True))

        assert returned_names == expected_names

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == Actor.objects.count()

    def test_list_actors_without_permissions(self):

        url = reverse('actor-create-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN, (
            "Esperado 403 para usuário sem permissão de acesso."
        )

    def test_list_actors_user_not_authenticated(self):
        self.client.logout()
        url = reverse('actor-create-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f"Esperado 401 para usuário não autenticado, retornou {response.status_code}"
        )

    def test_create_actor_success(self, actor_data):
        self.give_permissions(model=Actor)

        url = reverse('actor-create-list')
        response = self.client.post(
            url, actor_data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Actor.objects.filter(name=actor_data['name']).exists()

    def test_create_actor_without_permission(self, actor_data):
        url = reverse('actor-create-list')
        response = self.client.post(
            url, actor_data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Actor.objects.filter(name=actor_data['name']).exists()

    def test_create_actor_user_not_authenticated(self, actor_data):
        self.client.logout()
        self.give_permissions(model=Actor)

        url = reverse('actor-create-list')
        response = self.client.post(
            url, actor_data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Actor.objects.filter(name=actor_data['name']).exists()

    def test_update_actor_success(self, existing_actor):
        self.give_permissions(model=Actor)

        id = existing_actor.id
        data = {'name': faker_gen.name_female()}
        url = reverse('actor-detail-view', kwargs={'pk': id})
        response = self.client.patch(
            url, data
        )

        existing_actor.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert existing_actor.name == data['name']

    def test_update_actor_without_permissions(self, existing_actor):
        id = existing_actor.id
        data = {'name': faker_gen.name_female()}
        url = reverse('actor-detail-view', kwargs={'pk': id})
        response = self.client.patch(
            url, data
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not existing_actor.name == data['name']

    def test_update_actor_user_not_authenticated(self, existing_actor):
        self.client.logout()

        id = existing_actor.id
        data = {'name': faker_gen.name_female()}
        url = reverse('actor-detail-view', kwargs={'pk': id})
        response = self.client.patch(
            url, data
        )

        existing_actor.refresh_from_db()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not existing_actor.name == data['name']

    def test_delete_actor_success(self, existing_actor):
        self.give_permissions(model=Actor)

        id = existing_actor.id
        actor_name = existing_actor.name

        url = reverse('actor-detail-view', kwargs={'pk': id})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Actor.objects.filter(name=actor_name).exists()

    def test_delete_actor_without_permissions(self, existing_actor):
        id = existing_actor.id
        url = reverse('actor-detail-view', kwargs={'pk': id})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Actor.objects.filter(name=existing_actor.name).exists()

    def test_delete_actor_user_not_authenticated(self, existing_actor):
        self.client.logout()

        id = existing_actor.id
        url = reverse('actor-detail-view', kwargs={'pk': id})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Actor.objects.filter(name=existing_actor.name).exists()
