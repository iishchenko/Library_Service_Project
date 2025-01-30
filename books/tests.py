from django.test import TestCase
from django.contrib.auth import get_user_model
from books.models import Book
from django.utils import timezone


class UserModelTest(TestCase):

    def test_user_creation(self):
        user = get_user_model().objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
        )
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(user.phone_number, "0123456789")

    def test_user_phone_number(self):
        user = get_user_model().objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
            phone_number="1234567890"
        )
        self.assertEqual(user.phone_number, "1234567890")

    def test_user_name_default(self):
        user = get_user_model().objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123"
        )
        self.assertEqual(user.name, "Default Name")

#    def test_user_image(self):
#        user = get_user_model().objects.create_user(
#            email="testuser@example.com",
#            username="testuser",
#            password="password123"
#        )
#        # Assert that the image field is None, which is expected behavior
#        self.assertIs(user.image, None)

    def test_user_code_agency(self):
        user = get_user_model().objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
            code_agency=10
        )
        self.assertEqual(user.code_agency, 10)


class BookModelTest(TestCase):

    def test_book_creation(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            published_date=timezone.now(),
            isbn="1234567890123",
            pages=200,
            cover="SOFT",
            language="English",
        )
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.isbn, "1234567890123")
        self.assertEqual(book.pages, 200)
        self.assertEqual(book.cover, "SOFT")
        self.assertEqual(book.language, "English")

    def test_book_str_method(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            published_date=timezone.now(),
            isbn="1234567890123",
            pages=200,
            cover="SOFT",
            language="English",
        )
        self.assertEqual(str(book), "Test Book by Test Author")
