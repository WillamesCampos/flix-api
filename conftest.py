import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from actors.tests.factories import ActorFactory
from app.test_settings import faker_gen
from genres.models import Genre
from genres.tests.factories import GenreFactory
from reviews.tests.factories import ReviewFactory

User = get_user_model()


@pytest.fixture
def genre_factory():
    return GenreFactory()


@pytest.fixture
def list_of_actors_id_factory():
    return [ActorFactory().uuid for _ in range(3)]


@pytest.fixture
def list_review_factory():
    return [ReviewFactory.create_batch(5), ReviewFactory.create_batch(5), ReviewFactory.create_batch(5)]


@pytest.fixture
def movie_data(genre_factory, list_of_actors_id_factory):
    return {
        'title': 'Inception',
        'genre': genre_factory.uuid,
        'release_date': '2010-07-16',
        'actors': list_of_actors_id_factory,
        'resume': 'A thief who steals corporate secrets through the use of dream-sharing technology \
        is given the inverse task of planting an idea into the mind of a CEO.',
    }


@pytest.fixture
def user_with_permissions():
    user = User.objects.create_user(
        username=faker_gen.user_name(),
        email=faker_gen.email(),
        password=faker_gen.password(length=8),
    )

    group, _ = Group.objects.get_or_create(name='TestGroup')
    app_label = Genre._meta.app_label
    model_name = Genre._meta.model_name

    permissions = Permission.objects.filter(content_type__app_label=app_label, content_type__model=model_name)

    group.permissions.add(*permissions)
    group.user_set.add(user)
    user.refresh_from_db()

    return user


@pytest.fixture
def user_without_permissions():
    user = User.objects.create_user(
        username=faker_gen.user_name(),
        email=faker_gen.email(),
        password=faker_gen.password(length=8),
    )
    return user
