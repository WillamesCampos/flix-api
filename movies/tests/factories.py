from datetime import datetime

import factory

from actors.tests.factories import ActorFactory
from app.test_settings import faker_gen
from genres.tests.factories import GenreFactory
from movies.models import Movie

DEFAULT_ACTORS_COUNT = 3


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = faker_gen.sentence(nb_words=3)
    genre = factory.SubFactory(GenreFactory)
    release_date = faker_gen.date(end_datetime=datetime.now())
    resume = faker_gen.text(max_nb_chars=500)

    @factory.post_generation
    def actors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.actors.set(extracted)
        else:
            default_actors = ActorFactory.create_batch(DEFAULT_ACTORS_COUNT)
            self.actors.set(default_actors)
