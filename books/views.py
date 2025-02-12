from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction
from books.models import Book, Borrowing, Payment
from books.serializers import (
    BookSerializer,
    UserSerializer,
    RegisterUserSerializer,
    BorrowingSerializer,
    PaymentSerializer,
)
from rest_framework.decorators import action


User = get_user_model()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class BorrowingViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        user_id = self.request.query_params.get('user_id')
        is_active = self.request.query_params.get('is_active')

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(actual_return_date__isnull=True)
            else:
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        book = get_object_or_404(Book, id=book_id)

        if book.inventory <= 0:
            return Response({"error": "Book is out of stock."}, status=status.HTTP_400_BAD_REQUEST)

        due_date = timezone.now() + timezone.timedelta(days=14)
        borrowing = Borrowing.objects.create(book=book, user=request.user, due_date=due_date)

        book.inventory -= 1
        book.save()

        send_telegram_notification(f"New borrowing created: {borrowing.id}")

        serializer = self.get_serializer(borrowing)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response({"error": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST)

        borrowing.actual_return_date = timezone.now()
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        send_telegram_notification(f"Book returned: {borrowing.id}")

        serializer = self.get_serializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, borrowing_id=None):
        borrowing = get_object_or_404(Borrowing, id=borrowing_id)

        if borrowing.user != request.user:
            return Response({"error": "You are not authorized to pay for this borrowing."}, status=status.HTTP_403_FORBIDDEN)

        if hasattr(borrowing, 'payment'):
            return Response({"error": "Payment already exists for this borrowing."}, status=status.HTTP_400_BAD_REQUEST)

        amount = request.data.get("amount")
        if not amount:
            return Response({"error": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            borrowing=borrowing,
            user=request.user,
            amount=amount,
            payment_status='pending'
        )

        session = create_stripe_session(payment)
        payment.stripe_session_id = session.id
        payment.save()

        send_telegram_notification(f"Payment initiated: {payment.id}")

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        payment = get_object_or_404(Payment, id=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        payment = get_object_or_404(Payment, id=pk)

        if payment.payment_status == 'completed':
            return Response({"error": "Payment is already completed."}, status=status.HTTP_400_BAD_REQUEST)

        payment.payment_status = 'completed'
        payment.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
