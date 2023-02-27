from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from .filter import TitleFilter
from reviews.models import Title, Category, Genre
from users.permissions import IsAdminUserOrReadOnly
from .serializers import TitleSerializerCreate, CategorySerializer,\
    GenreSerializer, TitleSerializerList


class CreateListDestroy(mixins.CreateModelMixin,
                        mixins.ListModelMixin, mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатывем все типы запросов к произведениям."""
    queryset = (
        Title.objects.
        annotate(rating=(Avg('reviews__score'))).
        order_by('-pk')
    )

    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleSerializerCreate
        return TitleSerializerList


class CategoryViewSet(CreateListDestroy):
    """Обрабатывем все типы запросов к категориям."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroy):
    """Обрабатывем все типы запросов к жанрам."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'
