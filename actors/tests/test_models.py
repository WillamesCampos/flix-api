import pytest
import datetime

from django.db.utils import IntegrityError

from actors.models import Actor
from actors.models import NATIONALITY_CHOICES

from actors.tests.factories import ActorFactory


@pytest.mark.django_db
class TestModelActor:

    def __list_nationalities(self):
        return [choice[0] for choice in NATIONALITY_CHOICES]

    def test_create_actor_instance(self):
        obj = ActorFactory()

        assert isinstance(obj.name, str)
        assert isinstance(obj.birthday, datetime.date)
        assert isinstance(obj.nationality, str)

        assert obj.nationality in self.__list_nationalities()

        assert Actor.objects.filter(name=obj.name).exists()

    def test_create_actor_without_name(self):
        with pytest.raises(IntegrityError):
            ActorFactory(name=None)

    def test_create_actor_without_birthday(self):
        obj = ActorFactory(birthday=None)

        assert Actor.objects.filter(name=obj.name).exists()
        assert not obj.birthday

    def test_create_actor_without_nationality(self):

        obj = ActorFactory(nationality=None)

        assert Actor.objects.filter(name=obj.name).exists()
        assert not obj.nationality
