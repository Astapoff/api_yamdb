from os import listdir
from os.path import isfile, join
import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from api.serializers import (CategorySerializer,
                             TitleSerializerCreate,
                             GenreSerializer,
                             GenreTitleSerializer)
from reviews.serializers import (ReviewSerializer,
                                 CommentSerializer)
from users.serializers import CustomUserSerializer


def handle_category_csv(file_path):
    """Импорт данных из static/data/category.csv"""
    with open(file_path) as fp:
        reader = csv.DictReader(fp)
        for i in reader:
            a = CategorySerializer(data=i)
            if a.is_valid():
                a.id = i['id']
                a.save()
            print(a)


def handle_comments_csv(file_path):
    """Импорт данных из static/data/comments.csv"""
    with open(file_path) as fp:
        reader = csv.DictReader(fp)
        for i in reader:
            a = CommentSerializer(data=i)
            if a.is_valid():
                a.id = i['id']
                a.save()
            print(a)


def handle_genre_title_csv(file_path):
    """Импорт данных из static/data/genre_title.csv"""
    with open(file_path) as fp:
        reader = csv.DictReader(fp)
        for i in reader:
            a = GenreTitleSerializer(data=i)
            if a.is_valid():
                a.id = i['id']
                a.save()
            print(a)


def handle_genre_csv(file_path):
    """Импорт данных из static/data/genre.csv"""
    with open(file_path) as fp:
        reader = csv.DictReader(fp)
        for i in reader:
            a = GenreSerializer(data=i)
            if a.is_valid():
                a.id = i['id']
                a.save()
            print(a)


def handle_review_csv(file_path):
    """Импорт данных из static/data/review.csv"""
    with open(file_path) as fp:
        reader = csv.DictReader(fp)
        for i in reader:
            a = ReviewSerializer(data=i)
            if a.is_valid():
                a.id = i['id']
                a.save()
            print(a)


def handle_titles_csv(file_path):
    """Импорт данных из static/data/titles.csv"""
    with open(file_path) as fp:
        reader = csv.DictReader(fp)
        for i in reader:
            a = TitleSerializerCreate(data=i)
            if a.is_valid():
                a.id = i['id']
                a.save()
            print(a)


def handle_users_csv(file_path):
    """Импорт данных из static/data/users.csv"""
    with open(file_path) as fp:
        reader = csv.DictReader(fp)
        for i in reader:
            a = CustomUserSerializer(data=i)
            if a.is_valid():
                a.id = i['id']
                a.save()
            print(a)


class Command(BaseCommand):
    help = 'Импорт базы данных из CSV-файлов'
    file_map = {
        'category': handle_category_csv,
        'comments': handle_comments_csv,
        'genre_title': handle_genre_title_csv,
        'genre': handle_genre_csv,
        'review': handle_review_csv,
        'title': handle_titles_csv,
        'users': handle_users_csv,
    }

    def handle(self, *args, **options):
        csv_files = [
            f for f in listdir(
                settings.STATIC_DATA) if isfile(
                join(settings.STATIC_DATA, f))]
        for csv_file in csv_files:
            name = csv_file.split('.')[0]
            if name not in self.file_map:
                print('Нельзя обработать данный csv файл.')
                continue

            self.file_map[name](settings.STATIC_DATA / csv_file)
