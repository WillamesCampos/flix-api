from rest_framework import generics, response, status, views
from rest_framework.permissions import IsAuthenticated

from app.decorators import log_request
from app.permissions import GlobalDefaultPermission
from apps.core.adapters.ai_adapters.open_ai_adapter import OpenAIAdapter
from apps.movies.models import Movie
from apps.movies.serializers import (
    MovieDescriptionSerializer,
    MovieListDetailSerializer,
    MovieModelSerializer,
    MovieStatsSerializer,
)

from .mixins.movie_suggestor_description_mixin import MovieSuggestorDescriptionMixin
from .services.stats_service import stats_service


class BaseMovieAI:
    ai_adapter = OpenAIAdapter()


class MovieCreateListView(
    generics.ListCreateAPIView,
    MovieSuggestorDescriptionMixin,
    BaseMovieAI,
):
    created_instance = None
    permission_classes = (
        IsAuthenticated,
        GlobalDefaultPermission,
    )
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        self.created_instance = serializer.save(updated_by=self.request.user)

    @log_request
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        movie = self.created_instance
        if request.data.get('ai_description', False) and movie:
            description = self.suggest_description(movie)
            self.apply_description(movie, description)
            response.data['description'] = description

        return response


class MovieRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView,
    MovieSuggestorDescriptionMixin,
    BaseMovieAI,
):
    updated_instance = None
    permission_classes = (
        IsAuthenticated,
        GlobalDefaultPermission,
    )
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer

    @log_request
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        self.updated_instance = serializer.save(updated_by=self.request.user)

    @log_request
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        movie = self.updated_instance or self.get_object()

        if request.data.get('ai_description', False):
            description = self.suggest_description(movie)
            self.apply_description(movie, description)
            response.data['resume'] = description

        return response

    @log_request
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MovieStatsView(views.APIView):
    permission_classes = (
        IsAuthenticated,
        GlobalDefaultPermission,
    )
    pagination_class = None  # Disable pagination for stats endpoint
    queryset = Movie.objects.all()

    @log_request
    def get(self, request):
        service = stats_service(queryset=self.queryset)

        data = service.build_data()

        serializer = MovieStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return response.Response(data=serializer.validated_data, status=status.HTTP_200_OK)


class MovieSuggestorDescriptionView(views.APIView, MovieSuggestorDescriptionMixin, BaseMovieAI):
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def post(self, request):
        serializer = MovieDescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = serializer.validated_data['movie_uuid']

        description = self.suggest_description(movie)
        return response.Response(data={'description': description}, status=status.HTTP_200_OK)
