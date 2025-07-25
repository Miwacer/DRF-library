from rest_framework.viewsets import ModelViewSet, GenericViewSet

from book.models import Book
from book.permissions import IsAdminUserOrReadOnly
from book.serializers import (
    BookSerializer,
)


class BookViewSet(ModelViewSet, GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUserOrReadOnly,)