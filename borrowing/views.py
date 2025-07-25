from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingListForAdminSerializer,
)
from borrowing.telegram import send_telegram_message


class BorrowingViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        user = self.request.user

        if self.action == "list":
            if user.is_staff:
                return BorrowingListForAdminSerializer
            return BorrowingListSerializer
        elif self.action == "create":
            return BorrowingCreateSerializer
        elif self.action == "retrieve":
            return BorrowingDetailSerializer
        elif self.action in ["update", "partial_update"]:
            return BorrowingDetailSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        if is_active:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        if user.is_staff:
            if user_id:
                queryset = queryset.filter(user=user_id)

        return queryset

    @action(detail=True, methods=["PATCH"])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"detail": "Already returned."}, status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = timezone.now()
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()

        return Response(
            {"detail": "Book returned successfully."}, status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)

        message = (
            f"📚 New borrowing!\n"
            f" \n"
            f"Book: {borrowing.book.title}\n"
            f" \n"
            f"Expected return date: {borrowing.expected_return_date.strftime('%Y-%m-%d')}"
        )
        send_telegram_message(message)
