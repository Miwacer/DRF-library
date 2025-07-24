from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)

from library.models import Book, Borrowing
from library.permissions import IsAdminUserOrReadOnly
from library.serializers import (
    BookSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer
)


class BookViewSet(ModelViewSet, GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class BorrowingViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
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

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        return queryset


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
