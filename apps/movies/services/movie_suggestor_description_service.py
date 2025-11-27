from apps.core.adapters.ai_adapters.base import AIAgentAdapter
from apps.movies.models import Movie


class MovieSuggestorDescriptionService:
    def __init__(self, ai_adapter: AIAgentAdapter):
        self.ai_agent = ai_adapter

    def __build_prompt(self, movie: Movie) -> str:
        description = movie.resume or 'Not provided'
        prompt = f"""
        You are an expert in movies. You are responsible for suggesting a description for a movie: {movie.title} and description: {description}.
        The description should be a short summary of the movie.
        The description should be in the same language as the movie title.
        The description should be until 300 characters.
        Do not repeat the movie title in the description.
        Do not use the word "description" in the description.
        If the movie doesn't have a description, you should suggest a description based on the title.
        """

        return prompt

    def suggest_description(self, movie: Movie) -> str:
        prompt = self.__build_prompt(movie)
        description = self.ai_agent.answer(prompt)
        return description

    def apply_description(self, movie: Movie, description: str) -> None:
        movie.resume = description
        movie.save()
        return movie.refresh_from_db()
