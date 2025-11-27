import factory

from app.tests import faker_gen


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'genres.Genre'

    uuid = factory.LazyAttribute(lambda x: faker_gen.uuid4())
    name = factory.Faker('word')
