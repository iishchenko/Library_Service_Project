from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from books.models import Book
from books.serializers import BookSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from books.serializers import UserSerializer, RegisterUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

User = get_user_model()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
