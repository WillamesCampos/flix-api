from django.urls import path

from . import views

urlpatterns = [
    path(
        'actors/',
        views.ActorCreateListView.as_view(),
        name='actor-create-list',
    ),
    path(
        'actors/<uuid:pk>/',
        views.ActorRetrieveUpdateDestroyView.as_view(),
        name='actor-detail-view',
    ),
]
