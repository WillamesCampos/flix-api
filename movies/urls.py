from django.urls import path

from . import views

urlpatterns = [
    path(
        'movies/',
        views.MovieCreateListView.as_view(),
        name='movie-create-list',
    ),
    path(
        'movies/<uuid:pk>/',
        views.MovieRetrieveUpdateDestroyView.as_view(),
        name='movie-detail-view',
    ),
    path(
        'movies/stats/',
        views.MovieStatsView.as_view(),
        name='movie-stats-view',
    ),
    path(
        'movies/suggest-description/',
        views.MovieSuggestorDescriptionView.as_view(),
        name='movie-suggestor-description-view',
    ),
]
