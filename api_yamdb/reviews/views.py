from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Title, Review
from .serializers import ReviewSerializer, CommentSerializer
from users.permissions import NotUserRoleOrIsAuthor, ReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (NotUserRoleOrIsAuthor | ReadOnly,)

    def perform_update(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if Review.objects.filter(author=self.request.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (NotUserRoleOrIsAuthor | ReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author=self.request.user,
            review=review
        )
