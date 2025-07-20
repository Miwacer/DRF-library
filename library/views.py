from rest_framework.viewsets import ModelViewSet, GenericViewSet

from library.models import Book
from library.permissions import  IsAdminUserOrReadOnly
from library.serializers import BookSerializer


class BookViewSet(ModelViewSet, GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUserOrReadOnly, )