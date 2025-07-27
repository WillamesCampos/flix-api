import factory
from factory import fuzzy

from actors.models import NATIONALITY_CHOICES, Actor
from app.test_settings import faker_gen


class ActorFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda name: faker_gen.name_male())
    birthday = factory.LazyAttribute(
        lambda birthday: faker_gen.date_of_birth(
            minimum_age=18, maximum_age=99
        )
    )
    nationality = fuzzy.FuzzyChoice([
        choice[0] for choice in NATIONALITY_CHOICES
    ])

    class Meta:
        model = Actor
