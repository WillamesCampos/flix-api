from django.db.models import QuerySet, Count, Avg
from reviews.models import Review


class MovieStatsService:

    def __init__(self, queryset: QuerySet) -> None:
        self.queryset = queryset
        self.reviews = Review.objects.count()

    def __get_total_movies(self) -> int:
        return self.queryset.count()

    def __get_movies_by_genre(self) -> int:
        return self.queryset.values('genre__name').annotate(count=Count('id'))

    def __get_average_stars(self) -> float:
        average_stars = round(
            Review.objects.aggregate(
                avg_stars=Avg('stars')
            )['avg_stars'], 1
        )

        return average_stars if average_stars else 0

    def build_data(self):
        data = {
            'total_movies': self.__get_total_movies(),
            'movies_by_genre': self.__get_movies_by_genre(),
            'total_reviews': self.reviews,
            'average_stars': self.__get_average_stars()
        }

        return data
