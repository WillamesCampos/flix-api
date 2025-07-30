import pytest

from movies.serializers import MovieModelSerializer


@pytest.mark.django_db
class TestMovieModelSerializer:
    def setup_method(self):
        self.serializer = MovieModelSerializer

    def test_movie_serializer_valid_data(self, movie_data):
        serializer = self.serializer(data=movie_data)

        assert serializer.is_valid()

        validated = serializer.validated_data

        assert movie_data['title'] == validated['title']
        assert movie_data['genre'] == validated['genre'].id
        assert movie_data['release_date'] == validated['release_date'].strftime('%Y-%m-%d')
        assert movie_data['resume'] == validated['resume']

    def test_movie_serializer_invalid_data_release_date(self, movie_data):
        movie_data['release_date'] = '1899-12-31'
        serializer = self.serializer(data=movie_data)

        assert not serializer.is_valid()
        assert 'release_date' in serializer.errors

        assert f'The release date can not be less than {self.serializer.LIMIT_YEAR_OF_BIRTH}.' == str(serializer.errors['release_date'][0])

    def test_movie_serializer_invalid_data_resume(self, movie_data):
        movie_data['resume'] = 'A' * (self.serializer.LIMIT_RESUME_CHARACTERS + 1)
        serializer = self.serializer(data=movie_data)

        assert not serializer.is_valid()
        assert 'resume' in serializer.errors

        assert f'The resume can not have lenght more than {self.serializer.LIMIT_RESUME_CHARACTERS} characters' == str(serializer.errors['resume'][0])

    def test_movie_serializer_invalid_data_genre(self, movie_data):
        movie_data['genre'] = None
        serializer = self.serializer(data=movie_data)

        assert not serializer.is_valid()
        assert 'genre' in serializer.errors

        assert 'This field may not be null.' == str(serializer.errors['genre'][0])

    def test_movie_serializer_invalid_data_actors(self, movie_data):
        movie_data['actors'] = []
        serializer = self.serializer(data=movie_data)

        assert not serializer.is_valid()
        assert 'actors' in serializer.errors

        assert 'This list may not be empty.' == str(serializer.errors['actors'][0])

    def test_movie_serializer_invalid_data_title(self, movie_data):
        movie_data['title'] = ''
        serializer = self.serializer(data=movie_data)

        assert not serializer.is_valid()
        assert 'title' in serializer.errors

        assert 'This field may not be blank.' == str(serializer.errors['title'][0])
