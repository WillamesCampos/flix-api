from rest_framework import serializers

from movies.models import Movie
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewUpdateSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), required=False)

    class Meta:
        model = Review
        fields = '__all__'
