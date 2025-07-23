from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from library.models import Book, Borrowing


class BookSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(BookSerializer, self).validate(attrs)
        Book.validate_inventory_count(attrs["inventory"])

        return data

    class Meta:
        model = Book
        fields = ("id", "title", "cover", "inventory", "daily_fee")


class BorrowingSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "book_title",
            "user"
        )

    def create(self, validated_data):
        book = validated_data["book"]

        if book.inventory < 1:
            raise ValidationError(f"{book.title}: Out of stock")

        book.inventory -= 1
        book.save()

        return super().create(validated_data)