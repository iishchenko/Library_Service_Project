from rest_framework.views import APIView
from books.models import Book, Borrowing
from books.serializers import BookSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from books.serializers import UserSerializer, RegisterUserSerializer, BorrowingSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

User = get_user_model()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class BorrowBookAPIView(APIView):
    def post(self, request, book_id, *args, **kwargs):
        # Get the book object by its ID
        book = get_object_or_404(Book, id=book_id)

        # Get the current logged-in user
        user = request.user

        # Set the due date (e.g., 14 days from now)
        due_date = timezone.now() + timezone.timedelta(days=14)

        # Create a borrowing record
        borrowing = Borrowing.objects.create(book=book, user=user, due_date=due_date)

        # Serialize the borrowing data
        serializer = BorrowingSerializer(borrowing)

        return Response({"message": "Book borrowed!"}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        # Retrieve the borrowed book details based on the provided pk (primary key)
        book_id = kwargs.get('pk')  # Get the book ID from the URL path
        try:
            # Fetch the book from the database
            borrowed_book = BorrowedBook.objects.get(id=book_id)
        except BorrowedBook.DoesNotExist:
            return Response({"error": "Borrowed book not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data to return in the response
        serializer = BorrowingSerializer(borrowed_book)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)