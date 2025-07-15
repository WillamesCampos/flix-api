import factory


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'genres.Genre'

    name = factory.Faker('word')