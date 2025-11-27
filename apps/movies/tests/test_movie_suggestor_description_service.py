from unittest.mock import MagicMock

import pytest

from apps.movies.services.movie_suggestor_description_service import MovieSuggestorDescriptionService
from apps.movies.tests.factories import MovieFactory


@pytest.mark.django_db
class TestMovieSuggestorDescriptionService:
    def setup_method(self):
        self.mock_adapter = MagicMock()
        self.service = MovieSuggestorDescriptionService(ai_adapter=self.mock_adapter)

    def test_suggest_description_calls_adapter_with_movie_context(self):
        # Arrange
        movie = MovieFactory(title='Inception', resume='Mind-bending thriller')
        self.mock_adapter.answer.return_value = 'Generated description'

        # Act
        result = self.service.suggest_description(movie)

        # Assert
        self.mock_adapter.answer.assert_called_once()
        prompt = self.mock_adapter.answer.call_args[0][0]
        assert 'Inception' in prompt
        assert 'Mind-bending thriller' in prompt
        assert '300 characters' in prompt
        assert result == 'Generated description'

    def test_suggest_description_handles_missing_resume(self):
        # Arrange
        movie = MovieFactory(resume=None)
        self.mock_adapter.answer.return_value = 'Description without resume'

        # Act
        self.service.suggest_description(movie)

        # Assert
        prompt = self.mock_adapter.answer.call_args[0][0]
        assert 'Not provided' in prompt

    def test_apply_description_updates_movie_resume(self):
        # Arrange
        movie = MovieFactory(resume='Old description')
        new_description = 'Fresh synopsis from AI'

        # Act
        self.service.apply_description(movie, new_description)

        # Assert
        movie.refresh_from_db()
        assert movie.resume == new_description
