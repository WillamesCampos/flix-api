from unittest.mock import MagicMock

import pandas as pd
import pytest

from actors.tests.factories import ActorFactory
from genres.tests.factories import GenreFactory
from movies.models import Movie
from movies.services.import_service import MovieImportService


@pytest.fixture
def genre():
    return GenreFactory(name='Action')


@pytest.fixture
def actor1():
    return ActorFactory(name='Actor One')


@pytest.fixture
def actor2():
    return ActorFactory(name='Actor Two')


@pytest.fixture
def dataframe_file_valid(genre, actor1, actor2):
    return pd.DataFrame({
        'title': ['Test Movie'],
        'genre': [genre.name],
        'release_date': ['2020-01-01'],
        'actors': [f'{actor1.name}, {actor2.name}'],
        'resume': ['A test movie resume'],
    })


@pytest.fixture
def dataframe_file_empty():
    return pd.DataFrame({
        'title': [],
        'genre': [],
        'release_date': [],
        'actors': [],
        'resume': [],
    })


@pytest.fixture
def dataframe_file_multiple_movies(genre, actor1):
    return pd.DataFrame({
        'title': ['Test Movie', 'Test Movie 2'],
        'genre': [genre.name, genre.name],
        'release_date': ['2020-01-01', '2020-01-01'],
        'actors': [f'{actor1.name}, {actor2.name}', f'{actor1.name}, {actor2.name}'],
        'resume': ['A test movie resume', 'A test movie resume'],
    })


@pytest.mark.django_db
class TestMovieImportService:
    def setup_method(self):
        self.service_class = MovieImportService

    def test_import_movies_valid_data(self, dataframe_file_valid):
        # Arrange
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = dataframe_file_valid.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 1

        movie = Movie.objects.first()
        assert movie.title == 'Test Movie'
        assert movie.genre.name == 'Action'
        assert str(movie.release_date) == '2020-01-01'
        assert movie.resume == 'A test movie resume'
        assert movie.actors.count() == 2

    def test_import_movies_empty_file(self, dataframe_file_empty):
        # Arrange
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = dataframe_file_empty.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 0

    def test_import_movies_multiple_movies(self, dataframe_file_multiple_movies):
        # Arrange
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = dataframe_file_multiple_movies.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 2
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 2

    def test_import_movies_missing_title(self, genre):
        # Arrange
        movie_without_title = pd.DataFrame({
            'title': [''],
            'genre': [genre.name],
            'release_date': ['2020-01-01'],
            'actors': [f'{actor1.name}, {actor2.name}'],
            'resume': ['A test movie resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_without_title.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Title is required' in result['errors'][0]
        assert Movie.objects.count() == 0

    def test_import_movies_missing_genre(self):
        # Arrange
        movie_without_genre = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [''],
            'release_date': ['2020-01-01'],
            'actors': [f'{actor1.name}, {actor2.name}'],
            'resume': ['A test movie resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_without_genre.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)
        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Genre is required' in result['errors'][0]
        assert Movie.objects.count() == 0

    def test_import_movies_genre_not_found(self):
        # Arrange
        movie_genre_not_found = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': ['NonExistentGenre'],
            'release_date': ['2020-01-01'],
            'actors': [f'{actor1.name}, {actor2.name}'],
            'resume': ['A test movie resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_genre_not_found.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Genre "NonExistentGenre" not found. Create the genre first.' in result['errors'][0]
        assert Movie.objects.count() == 0

    def test_import_movies_invalid_date_format(self, genre):
        # Arrange
        movie_invalid_date_format = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [genre.name],
            'release_date': ['01-01-2020'],
            'actors': [f'{actor1.name}, {actor2.name}'],
            'resume': ['A test movie resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_invalid_date_format.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Invalid release date. Use the format YYYY-MM-DD' in result['errors'][0]
        assert Movie.objects.count() == 0

    def test_import_movies_valid_date_empty_string(self, genre):
        # Arrange
        movie_valid_date_empty_string = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [genre.name],
            'release_date': [''],
            'actors': [f'{actor1.name}, {actor2.name}'],
            'resume': ['A test movie resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_valid_date_empty_string.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 1

        movie = Movie.objects.first()
        assert movie.release_date is None

    def test_import_movies_resume_too_long(self, genre):
        # Arrange
        long_resume = 'A' * 501
        movie_resume_too_long = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [genre.name],
            'release_date': ['2020-01-01'],
            'actors': [f'{actor1.name}, {actor2.name}'],
            'resume': [long_resume],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_resume_too_long.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert 'Line 1: Resume exceeds 500 characters' in result['errors'][0]
        assert Movie.objects.count() == 0

    def test_import_movies_resume_empty(self, genre):
        # Arrange
        movie_resume_empty = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [genre.name],
            'release_date': ['2020-01-01'],
            'actors': [f'{actor1.name}, {actor2.name}'],
            'resume': [''],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_resume_empty.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 1

        movie = Movie.objects.first()
        assert movie.resume is None

    def test_import_movies_actors_exist(self, genre, actor1, actor2):
        # Arrange
        movie_actors_exist = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [genre.name],
            'release_date': ['2020-01-01'],
            'actors': [f'{actor1.name}, {actor2.name}'],
            'resume': ['A test movie resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_actors_exist.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 1

        movie = Movie.objects.first()
        movie_actors_uuid = list(map(str, movie.actors.values_list('uuid', flat=True)))
        assert actor1.uuid in movie_actors_uuid
        assert actor2.uuid in movie_actors_uuid

    def test_import_movies_actors_not_exist(self, genre):
        # Arrange
        movie_actors_not_exist = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [genre.name],
            'release_date': ['2020-01-01'],
            'actors': ['NonExistentActor1, NonExistentActor2'],
            'resume': ['A test movie resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_actors_not_exist.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 1

        movie = Movie.objects.first()
        movie_actors_uuid = list(map(str, movie.actors.values_list('uuid', flat=True)))
        assert 'NonExistentActor1' not in movie_actors_uuid
        assert 'NonExistentActor2' not in movie_actors_uuid

    def test_import_movies_actors_empty_string(self, genre):
        movie_actors_empty_string = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [genre.name],
            'release_date': ['2020-01-01'],
            'actors': [''],
            'resume': ['A test movie resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_actors_empty_string.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 1

    def test_import_movies_multiple_errors(self):
        # Arrange
        movie_multiple_errors = pd.DataFrame({
            'title': ['', 'Test Movie'],
            'genre': ['Action', 'NonExistentGenre'],
            'release_date': ['2020-01-01', '2020-01-01'],
            'actors': ['', ''],
            'resume': ['A test movie resume', 'A test movie resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_multiple_errors.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 0
        assert result['skipped_count'] == 2
        assert len(result['errors']) == 2
        assert 'Line 1: Title is required' in result['errors'][0]
        assert 'Line 2: Genre "NonExistentGenre" not found. Create the genre first.' in result['errors'][1]
        assert Movie.objects.count() == 0

    def test_import_movies_mixed_valid_invalid(self, genre):
        # Arrange
        movies_mixed = pd.DataFrame({
            'title': ['', 'Valid Movie'],
            'genre': [genre.name, genre.name],
            'release_date': ['2020-01-01', '2021-01-01'],
            'actors': ['', ''],
            'resume': ['', 'Valid resume'],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movies_mixed.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 1
        assert len(result['errors']) == 1
        assert Movie.objects.count() == 1

        movie = Movie.objects.first()
        assert movie.title == 'Valid Movie'

    def test_import_movies_date_with_spaces(self, genre):
        # Arrange
        movie_date_with_spaces = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [genre.name],
            'release_date': ['  2020-01-01  '],
            'actors': [''],
            'resume': [''],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_date_with_spaces.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 1

        movie = Movie.objects.first()
        assert str(movie.release_date) == '2020-01-01'

    def test_import_movies_resume_with_spaces(self, genre):
        # Arrange
        movie_resume_with_spaces = pd.DataFrame({
            'title': ['Test Movie'],
            'genre': [genre.name],
            'release_date': ['2020-01-01'],
            'actors': [''],
            'resume': ['  Resume with spaces  '],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_resume_with_spaces.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 1

        movie = Movie.objects.first()
        assert movie.resume == 'Resume with spaces'

    def test_import_movies_title_with_spaces(self, genre):
        # Arrange
        movie_title_with_spaces = pd.DataFrame({
            'title': ['  Test Movie  '],
            'genre': [genre.name],
            'release_date': ['2020-01-01'],
            'actors': [''],
            'resume': [''],
        })
        mock_file_reader = MagicMock()
        mock_file_reader.read.return_value = movie_title_with_spaces.to_dict(orient='records')
        service = self.service_class(file_path='test.csv', file_reader=mock_file_reader)

        # Act
        result = service.import_movies()

        # Assert
        assert result['created_count'] == 1
        assert result['skipped_count'] == 0
        assert len(result['errors']) == 0
        assert Movie.objects.count() == 1

        movie = Movie.objects.first()
        assert movie.title == 'Test Movie'
