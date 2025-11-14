import operator
from functools import reduce

from django.db.models import Q
from rest_framework import generics, response, status, views
from rest_framework.permissions import IsAuthenticated

from app.decorators import log_request
from app.permissions import GlobalDefaultPermission
from genres.models import Genre
from genres.serializers import GenreBulkCreateSerializer, GenreSerializer


class GenreCreateListView(generics.ListCreateAPIView):
    permission_classes = (
        IsAuthenticated,
        GlobalDefaultPermission,
    )
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @log_request
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class GenreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        GlobalDefaultPermission,
    )
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @log_request
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @log_request
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @log_request
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GenreBulkCreateView(views.APIView):
    permission_classes = (
        IsAuthenticated,
        GlobalDefaultPermission,
    )
    queryset = Genre.objects.all()

    @log_request
    def post(self, request):
        """
        Cria múltiplos gêneros em lote.
        Apenas cria gêneros que não existem no banco de dados.
        """
        serializer = GenreBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        genre_names = serializer.validated_data['genres']

        # Buscar gêneros que já existem (case-insensitive)
        # Construir query OR para buscar todos os nomes (case-insensitive)
        q_objects = [Q(name__iexact=name) for name in genre_names]
        if q_objects:
            existing_genres = Genre.objects.filter(reduce(operator.or_, q_objects)).values_list('name', flat=True)
            existing_names_lower = {name.lower() for name in existing_genres}
        else:
            existing_names_lower = set()

        # Filtrar apenas os gêneros que não existem
        genres_to_create = [name for name in genre_names if name.lower() not in existing_names_lower]

        # Criar os novos gêneros
        created_genres = []
        for genre_name in genres_to_create:
            genre = Genre.objects.create(name=genre_name)
            created_genres.append(GenreSerializer(genre).data)

        # Preparar resposta
        response_data = {
            'created': len(created_genres),
            'skipped': len(genre_names) - len(created_genres),
            'created_genres': created_genres,
            'skipped_genres': [name for name in genre_names if name.lower() in existing_names_lower],
        }

        return response.Response(data=response_data, status=status.HTTP_201_CREATED)
