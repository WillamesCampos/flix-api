from django.db.models import Avg
from rest_framework import serializers
from genres.serializers import GenreSerializer
from movies.models import Movie
from actors.serializers import ActorSerializer


class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_release_date(self, value):
        if value.year < 1900:
            raise serializers.ValidationError('The release date can not be less than 1990')

    def validate_resume(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('The resume can not have lenght more than 200 characters')


class MovieListDetailSerializer(serializers.ModelSerializer):

    actors = ActorSerializer(many=True)
    genre = GenreSerializer()
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'genre', 'actors', 'release_date', 'rate', 'resume'
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
