from apps.movies.models import Movie
from apps.movies.services.movie_suggestor_description_service import MovieSuggestorDescriptionService


class MovieSuggestorDescriptionMixin:
    def suggest_description(self, movie: Movie) -> str:
        suggestor_description_service = MovieSuggestorDescriptionService(ai_adapter=self.ai_adapter)
        description = suggestor_description_service.suggest_description(movie)

        return description

    def apply_description(self, movie: Movie, description: str) -> Movie:
        movie.resume = description
        movie.save()

        return movie
