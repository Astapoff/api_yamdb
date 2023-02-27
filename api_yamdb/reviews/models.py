from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='URL')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Жанр')
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='URL')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения')
    year = models.PositiveIntegerField(db_index=True)
    description = models.TextField(
        verbose_name='Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default='Категория не определена'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр произведения',
        blank=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, null=True, blank=True,
        on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)
    ])
    pub_date = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, null=True, blank=True,
        on_delete=models.CASCADE, related_name='comments',
    )
    text = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        ordering = ['genre']

    def __str__(self):
        return f'{self.title} в жанре {self.genre}'
