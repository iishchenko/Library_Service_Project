from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True, default="admin@example.com")
    phone_number = models.CharField(max_length=20, unique=True, default="0123456789")
    name = models.CharField(max_length=150, default="Default Name")
    image = models.ImageField(blank=True, null=True, default=None)
    date_joined = models.DateTimeField(default=timezone.now)
    code_agency = models.IntegerField(null=True, blank=True, default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    cover = models.CharField(
        max_length=20,
        choices=[
            ('SOFT', 'Softcover'),
            ('HARD', 'Hardcover'),
        ],
    )
    language = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} by {self.author}"
