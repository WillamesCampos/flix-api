from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from app.decorators import log_request
from app.permissions import GlobalDefaultPermission
from reviews.models import Review
from reviews.serializers import ReviewSerializer, ReviewUpdateSerializer


class ReviewCreateListView(generics.ListCreateAPIView):
    permission_classes = (
        IsAuthenticated,
        GlobalDefaultPermission,
    )
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @log_request
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        GlobalDefaultPermission,
    )
    queryset = Review.objects.all()
    serializer_class = ReviewUpdateSerializer

    @log_request
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @log_request
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @log_request
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
