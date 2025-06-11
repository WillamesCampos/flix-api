from rest_framework import generics
from rest_framework import views
from rest_framework import response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from movies.models import Movie
from movies.serializers import MovieListDetailSerializer
from movies.serializers import MovieModelSerializer
from movies.serializers import MovieStatsSerializer

from app.permissions import GlobalDefaultPermission
from .services import stats


class MovieCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer


class MovieRetrieveUpdateDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer


class MovieStatsView(views.APIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get(self, request):
        stats_service = stats.MovieStatsService(
            queryset=self.queryset
        )

        data = stats_service.build_data()

        serializer = MovieStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return response.Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK
        )
