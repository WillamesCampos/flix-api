from django.db.models import Avg
from rest_framework import serializers

from actors.serializers import ActorSerializer
from genres.serializers import GenreSerializer
from movies.models import Movie


class MovieModelSerializer(serializers.ModelSerializer):
    LIMIT_RESUME_CHARACTERS = 500
    LIMIT_YEAR_OF_BIRTH = 1900

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_release_date(self, value):
        if value.year < self.LIMIT_YEAR_OF_BIRTH:
            raise serializers.ValidationError('The release date can not be less than 1990')

    def validate_resume(self, value):
        if len(value) > self.LIMIT_RESUME_CHARACTERS:
            raise serializers.ValidationError('The resume can not have lenght more than 200 characters')


class MovieListDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)
    genre = GenreSerializer()
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'genre',
            'actors',
            'release_date',
            'rate',
            'resume',
        ]

    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        if rate:
            return round(rate, 1)
        return None


class MovieStatsSerializer(serializers.Serializer):
    total_movies = serializers.IntegerField()
    movies_by_genre = serializers.ListField()
    total_reviews = serializers.IntegerField()
    average_stars = serializers.FloatField()
