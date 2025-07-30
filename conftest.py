import pytest

from actors.tests.factories import ActorFactory
from genres.tests.factories import GenreFactory


@pytest.fixture
def genre_factory():
    return GenreFactory()


@pytest.fixture
def list_of_actors_id_factory():
    return [ActorFactory().id for _ in range(3)]
