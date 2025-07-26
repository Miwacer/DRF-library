from django.contrib.auth import get_user_model
from django.test import TestCase

from django.utils import timezone
from datetime import timedelta, datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer
)

from book.models import Book

BORROWING_URL = reverse("borrowing:borrowing-list")

def create_user():
    return get_user_model().objects.create_user(
        email=f"user{timezone.now().timestamp()}@test.com",
        password="test1234"
    )

def create_book(**params):
    timestamp = str(timezone.now().timestamp()).replace('.', '')
    unique_title = f"Book {timestamp}"

    defaults = {
        "title": unique_title,
        "cover": "Hard",
        "inventory": 5,
        "daily_fee": "1.00"
    }
    defaults.update(params)
    return Book.objects.create(**defaults)

def create_borrowing(user):
    book = create_book()
    borrowing = Borrowing.objects.create(
        borrow_date= timezone.now(),
        expected_return_date= timezone.now() + timedelta(days=3),
        actual_return_date=None,
        user=user,
        book=book
    )
    return borrowing


class UnauthorizedBorrowingApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

import pprint

class AuthorizedBorrowingApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)


    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_borrowing_list(self):
        create_borrowing(user=self.user)

        res = self.client.get(BORROWING_URL)
        borrowings = Borrowing.objects.filter(user=self.user)
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_borrowing_detail(self):
        borrowing = create_borrowing(user=self.user)
        url = reverse("borrowing:borrowing-detail", args=[borrowing.id])

        res = self.client.get(url)
        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_return_book(self):
        borrowing = create_borrowing(user=self.user)
        url = reverse("borrowings:borrowing-return-book", args=[borrowing.id])

        res = self.client.patch(url)

        self.assertEqual(res.data["detail"], "Book returned successfully.")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_return_book_twice(self):
        borrowing = create_borrowing(user=self.user)
        url = reverse("borrowing:borrowing-return-book", args=[borrowing.id])
        self.client.patch(url)
        res = self.client.patch(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["detail"], "Already returned.")

    def test_filter_active_borrowings_true(self):
        create_borrowing(user=self.user)

        res = self.client.get(BORROWING_URL, {"is_active": "true"})
        borrowings = Borrowing.objects.filter(user=self.user, actual_return_date__isnull=True)
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_active_borrowings_false(self):
        book = create_book()
        borrowing = Borrowing.objects.create(
            user=self.user,
            book=book,
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timedelta(days=2),
            actual_return_date=timezone.now()
        )

        res = self.client.get(BORROWING_URL, {"is_active": "false"})
        borrowings = Borrowing.objects.filter(user=self.user, actual_return_date__isnull=False)
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

