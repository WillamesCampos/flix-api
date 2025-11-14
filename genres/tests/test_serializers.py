from app.test_settings import faker_gen
from genres.serializers import GenreBulkCreateSerializer, GenreSerializer


class TestGenreSerializer:
    def setup_method(self):
        self.serializer = GenreSerializer

    def test_genre_serializer_valid_data(self):
        data = {
            'name': faker_gen.word(ext_word_list=['Action', 'Comedy', 'Drama']),
        }
        serializer = self.serializer(data=data)
        assert serializer.is_valid()
        validated = serializer.validated_data

        assert data['name'] == validated['name']

    def test_genre_serializer_invalid_data_name(self):
        data = {
            'name': '',
        }
        serializer = self.serializer(data=data)

        assert not serializer.is_valid()
        assert 'name' in serializer.errors

        assert 'This field may not be blank.' == str(serializer.errors['name'][0])

    def test_genre_serializer_invalid_data_name_as_number(self):
        data = {
            'name': 12345,
        }
        serializer = self.serializer(data=data)

        assert not serializer.is_valid()
        assert 'name' in serializer.errors

        assert 'A valid string is required.' == str(serializer.errors['name'][0])


class TestGenreBulkCreateSerializer:
    def setup_method(self):
        self.serializer = GenreBulkCreateSerializer

    def test_bulk_create_serializer_valid_data(self):
        """Testa serializer com dados válidos"""
        data = {'genres': ['Action', 'Comedy', 'Drama']}
        serializer = self.serializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['genres'] == ['Action', 'Comedy', 'Drama']

    def test_bulk_create_serializer_empty_list(self):
        data = {'genres': []}
        serializer = self.serializer(data=data)
        assert not serializer.is_valid()
        assert 'genres' in serializer.errors

    def test_bulk_create_serializer_empty_string_in_list(self):
        data = {'genres': ['Action', '', 'Comedy', '   ', 'Drama']}
        serializer = self.serializer(data=data)
        assert not serializer.is_valid()

    def test_bulk_create_serializer_numeric_genre(self):
        data = {'genres': ['Action', '12345', 'Comedy']}
        serializer = self.serializer(data=data)
        assert not serializer.is_valid()
        assert 'genres' in serializer.errors

    def test_bulk_create_serializer_removes_duplicates(self):
        data = {'genres': ['Action', 'action', 'ACTION', 'Comedy']}
        serializer = self.serializer(data=data)
        assert serializer.is_valid()
        validated_genres = serializer.validated_data['genres']

        assert len([g for g in validated_genres if g.lower() == 'action']) == 1
        assert 'Comedy' in validated_genres
