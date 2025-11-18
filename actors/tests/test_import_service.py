from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pandas as pd
import pytest

from actors.models import NATIONALITY_CHOICES, Actor
from actors.services.import_service import ActorImportService


@pytest.fixture
def dataframe_actor_valid():
    return pd.DataFrame({
        'name': ['John Doe'],
        'birthday': ['1990-01-01'],
        'nationality': ['USA'],
    })


@pytest.fixture
def dataframe_actor_empty():
    return pd.DataFrame({
        'name': [],
        'birthday': [],
        'nationality': [],
    })


@pytest.fixture
def dataframe_actor_multiple():
    return pd.DataFrame({
        'name': ['John Doe', 'Jane Smith'],
        'birthday': ['1990-01-01', '1985-05-15'],
        'nationality': ['USA', 'BRA'],
    })


@pytest.mark.django_db
class TestActorImportService:
    def setup_method(self):
        self.service_class = ActorImportService

    def test_import_actors_valid_data(self, dataframe_actor_valid):
        # Arrange
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = dataframe_actor_valid.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Actor.objects.count() == 1

        actor = Actor.objects.first()
        assert actor.name == 'John Doe'
        assert str(actor.birthday) == '1990-01-01'
        assert actor.nationality == 'USA'

    def test_import_actors_empty_file(self, dataframe_actor_empty):
        # Arrange
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = dataframe_actor_empty.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Actor.objects.count() == 0

    def test_import_actors_multiple_actors(self, dataframe_actor_multiple):
        # Arrange
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = dataframe_actor_multiple.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 2
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Actor.objects.count() == 2

    def test_import_actors_missing_name(self):
        # Arrange
        actor_without_name = pd.DataFrame({
            'name': [''],
            'birthday': ['1990-01-01'],
            'nationality': ['USA'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_without_name.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Name is required' in result['errors'][0]
        assert Actor.objects.count() == 0

    def test_import_actors_missing_birthday(self):
        # Arrange
        actor_without_birthday = pd.DataFrame({
            'name': ['John Doe'],
            'birthday': [''],
            'nationality': ['USA'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_without_birthday.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Invalid birthday. Must be in the format YYYY-MM-DD' in result['errors'][0]
        assert Actor.objects.count() == 0

    def test_import_actors_invalid_birthday_format(self):
        # Arrange
        actor_invalid_birthday_format = pd.DataFrame({
            'name': ['John Doe'],
            'birthday': ['01-01-1990'],
            'nationality': ['USA'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_invalid_birthday_format.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Invalid birthday. Must be in the format YYYY-MM-DD' in result['errors'][0]
        assert Actor.objects.count() == 0

    def test_import_actors_birthday_in_future(self):
        # Arrange
        future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        actor_birthday_future = pd.DataFrame({
            'name': ['John Doe'],
            'birthday': [future_date],
            'nationality': ['USA'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_birthday_future.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Birthday cannot be in the future' in result['errors'][0]
        assert Actor.objects.count() == 0

    def test_import_actors_invalid_nationality(self):
        # Arrange
        actor_invalid_nationality = pd.DataFrame({
            'name': ['John Doe'],
            'birthday': ['1990-01-01'],
            'nationality': ['INVALID'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_invalid_nationality.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Invalid nationality' in result['errors'][0]
        nationalities = [choice[0] for choice in NATIONALITY_CHOICES]
        assert ', '.join(nationalities) in result['errors'][0]
        assert Actor.objects.count() == 0

    def test_import_actors_nationality_empty(self):
        # Arrange
        actor_nationality_empty = pd.DataFrame({
            'name': ['John Doe'],
            'birthday': ['1990-01-01'],
            'nationality': [''],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_nationality_empty.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Actor.objects.count() == 1

        actor = Actor.objects.first()
        assert actor.name == 'John Doe'
        assert not actor.nationality

    def test_import_actors_multiple_errors(self):
        # Arrange
        actors_multiple_errors = pd.DataFrame({
            'name': ['', 'John Doe'],
            'birthday': ['1990-01-01', '1990-01-01'],
            'nationality': ['USA', 'INVALID'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actors_multiple_errors.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 2
        assert len(result['errors']) == 2
        assert 'Line 1: Name is required' in result['errors'][0]
        assert 'Line 2: Invalid nationality' in result['errors'][1]
        assert Actor.objects.count() == 0

    def test_import_actors_mixed_valid_invalid(self):
        # Arrange
        actors_mixed = pd.DataFrame({
            'name': ['', 'John Doe'],
            'birthday': ['1990-01-01', '1990-01-01'],
            'nationality': ['USA', 'USA'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actors_mixed.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert Actor.objects.count() == 1

        actor = Actor.objects.first()
        assert actor.name == 'John Doe'

    def test_import_actors_name_with_spaces(self):
        # Arrange
        actor_name_with_spaces = pd.DataFrame({
            'name': ['  John Doe  '],
            'birthday': ['1990-01-01'],
            'nationality': ['USA'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_name_with_spaces.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Actor.objects.count() == 1

        actor = Actor.objects.first()
        assert actor.name == 'John Doe'

    def test_import_actors_birthday_with_spaces(self):
        # Arrange
        actor_birthday_with_spaces = pd.DataFrame({
            'name': ['John Doe'],
            'birthday': ['  1990-01-01  '],
            'nationality': ['USA'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_birthday_with_spaces.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Actor.objects.count() == 1

        actor = Actor.objects.first()
        assert str(actor.birthday) == '1990-01-01'

    def test_import_actors_nationality_with_spaces(self):
        # Arrange
        actor_nationality_with_spaces = pd.DataFrame({
            'name': ['John Doe'],
            'birthday': ['1990-01-01'],
            'nationality': ['  USA  '],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_nationality_with_spaces.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Actor.objects.count() == 1

        actor = Actor.objects.first()
        assert actor.nationality == 'USA'

    def test_import_actors_valid_nationality_bra(self):
        # Arrange
        actor_bra = pd.DataFrame({
            'name': ['João Silva'],
            'birthday': ['1990-01-01'],
            'nationality': ['BRA'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_bra.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Actor.objects.count() == 1

        actor = Actor.objects.first()
        assert actor.nationality == 'BRA'

    def test_import_actors_valid_nationality_usa(self):
        # Arrange
        actor_usa = pd.DataFrame({
            'name': ['John Doe'],
            'birthday': ['1990-01-01'],
            'nationality': ['USA'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = actor_usa.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_actors()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Actor.objects.count() == 1

        actor = Actor.objects.first()
        assert actor.nationality == 'USA'
