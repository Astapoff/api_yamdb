from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE = [
        ('user', USER),
        ('moderator', MODERATOR),
        ('admin', ADMIN),
    ]
    role = models.CharField(
        max_length=40, choices=ROLE,
        default=USER, verbose_name='Роль',
    )
    email = models.EmailField(max_length=60, blank=False, unique=True)
    bio = models.TextField(max_length=250, blank=True)

    class Meta:
        ordering = ('-pk',)

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    def save(self, *args, **kwargs):
        if self.role == self.MODERATOR:
            self.is_staff = True
        if self.role == self.ADMIN:
            self.is_superuser = True
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
