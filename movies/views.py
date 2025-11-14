from rest_framework import generics, response, status, views
from rest_framework.permissions import IsAuthenticated

from app.decorators import log_request
from app.permissions import GlobalDefaultPermission
from movies.models import Movie
from movies.serializers import (
    MovieListDetailSerializer,
    MovieModelSerializer,
    MovieStatsSerializer,
)

from .services.stats_service import stats_service


class MovieCreateListView(generics.ListCreateAPIView):
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

    @log_request
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
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

    @log_request
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

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
