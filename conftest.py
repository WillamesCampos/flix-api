import pytest

from actors.tests.factories import ActorFactory
from genres.tests.factories import GenreFactory


@pytest.fixture
def genre_factory():
    return GenreFactory()


@pytest.fixture
def list_of_actors_id_factory():
    return [ActorFactory().id for _ in range(3)]


@pytest.fixture
def movie_data(genre_factory, list_of_actors_id_factory):
    return {
        'title': 'Inception',
        'genre': genre_factory.id,
        'release_date': '2010-07-16',
        'actors': list_of_actors_id_factory,
        'resume': 'A thief who steals corporate secrets through the use of dream-sharing technology \
        is given the inverse task of planting an idea into the mind of a CEO.',
    }
