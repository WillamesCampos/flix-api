from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from actors.models import Actor
from actors.serializers import ActorSerializer
from app.decorators import log_request
from app.permissions import GlobalDefaultPermission


class ActorCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @log_request
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ActorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        GlobalDefaultPermission,
    )
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    @log_request
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @log_request
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @log_request
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
