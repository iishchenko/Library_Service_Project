from rest_framework.routers import DefaultRouter
from django.urls import path, include
from books.views import BookViewSet,RegisterUserView, UserListView, BorrowBookAPIView

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")

# Define the URL patterns
urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("api/", include(router.urls)),  # Include the book-related routes
    path('borrow/<int:book_id>/', BorrowBookAPIView.as_view(), name='borrow-book'),
    path('borrowed/<int:pk>/', BorrowBookAPIView.as_view(), name='borrow-book-detail'),
]