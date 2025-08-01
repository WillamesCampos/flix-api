import factory

from app.test_settings import faker_gen
from movies.tests.factories import MovieFactory
from reviews.models import Review


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    stars = factory.LazyAttribute(lambda stars: faker_gen.random_int(min=1, max=5))
    comment = factory.LazyAttribute(lambda comment: faker_gen.text(max_nb_chars=200))
    movie = factory.SubFactory(MovieFactory)
