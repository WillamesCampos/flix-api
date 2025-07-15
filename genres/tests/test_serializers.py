import pytest
from app.test_settings import faker_gen

from genres.serializers import GenreSerializer


class TestGenreSerializer:
    def setup_method(self):
        self.serializer = GenreSerializer

    def test_genre_serializer_valid_data(self):
        data = {
            "name": faker_gen.word(ext_word_list=['Action', 'Comedy', 'Drama']),
        }
        serializer = self.serializer(data=data)
        assert serializer.is_valid()
        validated = serializer.validated_data

        assert data['name'] == validated['name']

    def test_genre_serializer_invalid_data_name(self):
        data = {
            "name": "",
        }
        serializer = self.serializer(data=data)

        assert not serializer.is_valid()
        assert 'name' in serializer.errors

        assert 'This field may not be blank.' == str(serializer.errors['name'][0])

    def test_genre_serializer_invalid_data_name_as_number(self):
        data = {
            "name": 12345,
        }
        serializer = self.serializer(data=data)

        assert not serializer.is_valid()
        assert 'name' in serializer.errors

        assert 'A valid string is required.' == str(serializer.errors['name'][0])
