from rest_framework import serializers
from reviews.models import Title, Category, Genre, GenreTitle


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Title."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreTitleSerializer(serializers.ModelSerializer):
    """Сериализатор связанных моделей Title и Genre"""

    class Meta:
        fields = ('id', 'genre', 'title')
        model = GenreTitle


class TitleSerializerList(serializers.ModelSerializer):
    """Сериализатор модели Title."""
    genre = GenreSerializer(many=True,)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year',
            'description', 'category', 'genre', 'rating')
        model = Title


class TitleSerializerCreate(serializers.ModelSerializer):
    """Сериализатор модели Title."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title
