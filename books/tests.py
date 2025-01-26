from rest_framework.test import APITestCase
from rest_framework import status
from books.models import Book


class BookAPITests(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Example Book",
            author="John Doe",
            published_date="2020-01-01",
            isbn="1234567890123",
            pages=200,
            cover="HARD",
            language="English",
        )

    def test_list_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_book(self):
        response = self.client.get(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "Jane Doe",
            "published_date": "2021-01-01",
            "isbn": "9876543210987",
            "pages": 150,
            "cover": "SOFT",
            "language": "English",
        }
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Only admins can create
