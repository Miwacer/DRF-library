from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.models import Book


class BookSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(BookSerializer, self).validate(attrs)
        Book.validate_inventory_count(attrs["inventory"])

        return data

    class Meta:
        model = Book
        fields = ("id", "title", "cover", "inventory", "daily_fee")


class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "cover", "daily_fee")
