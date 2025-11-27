import factory

from app.test_settings import faker_gen
from apps.movies.tests.factories import MovieFactory
from apps.reviews.models import Review


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    uuid = factory.LazyAttribute(lambda x: faker_gen.uuid4())
    stars = factory.LazyAttribute(lambda stars: faker_gen.random_int(min=1, max=5))
    comment = factory.LazyAttribute(lambda comment: faker_gen.text(max_nb_chars=200))
    movie = factory.SubFactory(MovieFactory)
