from rest_framework import serializers

from apps.genres.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if str.isnumeric(value):
            raise serializers.ValidationError('A valid string is required.')
        return value

    class Meta:
        model = Genre
        fields = '__all__'


class GenreBulkCreateSerializer(serializers.Serializer):
    genres = serializers.ListField(child=serializers.CharField(max_length=200), min_length=1, help_text='Lista de nomes de gêneros para criar')

    def validate_genres(self, value):
        if not value:
            raise serializers.ValidationError('A lista de gêneros não pode estar vazia.')

        seen = set()
        unique_genres = []
        for genre in value:
            genre_name = genre.strip()
            if not genre_name:
                continue
            if str.isnumeric(genre_name):
                raise serializers.ValidationError(f'"{genre_name}" não é um nome válido. Números não são permitidos.')
            if genre_name.lower() not in seen:
                seen.add(genre_name.lower())
                unique_genres.append(genre_name)

        return unique_genres
