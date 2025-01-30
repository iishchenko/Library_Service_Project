from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True, default="admin@example.com")
    phone_number = models.CharField(max_length=20, unique=True, default="0123456789")
    name = models.CharField(max_length=150, default="Default Name")
    image = models.ImageField(blank=True, null=True, default=None, upload_to='images/')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = 'books_user'
        verbose_name = "user"
        verbose_name_plural = "users"


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
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrowings')
    date_borrowed = models.DateField(auto_now_add=True)  # Automatically sets the date when borrowing occurs
    date_returned = models.DateField(null=True, blank=True)  # Can be null if the book hasn't been returned yet
    due_date = models.DateField(null=True, blank=True)
    is_returned = models.DateTimeField(default=False)

    def __str__(self):
        return f"{self.user} borrowed {self.book} on {self.date_borrowed}"

    class Meta:
        unique_together = ('user', 'book', 'date_borrowed')
