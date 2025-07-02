import datetime
import pytest

from actors.serializers import ActorSerializer
from actors.tests.factories import ActorFactory
from app.test_settings import faker_gen


@pytest.mark.django_db
class TestActorSerializer:

    def setup_method(self):
        self.serializer = ActorSerializer

    def test_actor_serializer_valid_data(self):
        data = {
            "name": faker_gen.name_male(),
            "birthday": faker_gen.date_of_birth(),
            "nationality": "USA"
        }
        serializer = self.serializer(data=data)

        assert serializer.is_valid()

        validated = serializer.validated_data

        assert data['name'] == validated['name']
        assert data['birthday'] == validated['birthday']
        assert data['nationality'] == validated['nationality']

    def test_actor_serializer_invalid_data_name(self):
        data = {
            "name": "",
            "birthday": datetime.date(day=25, month=10, year=2001),
            "nationality": "BRA"
        }
        serializer = self.serializer(data=data)

        assert not serializer.is_valid()
        assert 'name' in serializer.errors

        assert 'This field may not be blank.' == str(serializer.errors['name'][0])

    def test_actor_serializer_invalid_data_birthday(self):
        data = {
            "name": faker_gen.name_female(),
            "birthday": "Not-a-date",
            "nationality": "BRA"
        }
        serializer = self.serializer(data=data)

        assert not serializer.is_valid()
        assert 'birthday' in serializer.errors

        assert 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.' == str(serializer.errors['birthday'][0])

    def test_actor_serializer_invalid_data_nationality(self):
        data = {
            "name": faker_gen.name_female(),
            "birthday": datetime.date(day=25, month=10, year=2001),
            "nationality": "NOT-IN-CHOICES"
        }
        serializer = self.serializer(data=data)

        assert not serializer.is_valid()
        assert 'nationality' in serializer.errors

        assert '"NOT-IN-CHOICES" is not a valid choice.' == str(serializer.errors['nationality'][0])

    def test_actor_serializer_output(self):

        obj = ActorFactory()
        serializer = self.serializer(instance=obj)

        assert serializer.data['name'] == obj.name
        assert serializer.data['birthday'] == obj.birthday.isoformat()
        assert serializer.data['nationality'] == obj.nationality
