from rest_framework.routers import DefaultRouter
from django.urls import path, include
from books.views import (
    BookViewSet,
    RegisterUserView,
    UserDetailView,
    BorrowingViewSet,
    PaymentViewSet,
)

# Initialize the router
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'borrowings', BorrowingViewSet, basename='borrowing')
router.register(r'payments', PaymentViewSet, basename='payment')

# Define the URL patterns
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('users/me/', UserDetailView.as_view(), name='user-detail'),
    path('', include(router.urls)),  # Include the routes managed by the router
]
