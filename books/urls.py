from rest_framework.routers import DefaultRouter
from books.views import BookViewSet
from django.urls import path, include
from books.views import RegisterUserView, UserListView

router = DefaultRouter()
router.register(r'books', BookViewSet, basename="book")

urlpatterns = [
    path('api/', include(router.urls)),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("", UserListView.as_view(), name="user-list"),
    path('books/', BookViewSet.as_view({'post': 'create'}), name='book-create'),
]
