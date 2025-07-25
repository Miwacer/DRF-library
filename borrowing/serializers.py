from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowing.models import Borrowing
from book.serializers import BookInfoSerializer

class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "book",
        )

    def create(self, validated_data):
        book = validated_data["book"]
        if book.inventory < 1:
            raise ValidationError(f"{book.title}: Out of stock")
        book.inventory -= 1
        book.save()
        return super().create(validated_data)


class BorrowingListSerializer(serializers.ModelSerializer):
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
        )


class BorrowingListForAdminSerializer(BorrowingListSerializer):
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
            "user",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookInfoSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
