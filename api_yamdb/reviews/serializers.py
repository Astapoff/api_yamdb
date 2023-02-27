from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Title, Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        request = self.context['request']
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    author=request.user, title=title
            ).exists():
                raise ValidationError(
                    'Вы уже оставили отзыв на это произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    text = serializers.CharField(allow_blank=False)

    class Meta:
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        model = Comment
