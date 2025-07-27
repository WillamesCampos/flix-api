from rest_framework import serializers

from genres.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if str.isnumeric(value):
            raise serializers.ValidationError('A valid string is required.')
        return value

    class Meta:
        model = Genre
        fields = '__all__'
