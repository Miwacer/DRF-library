from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from book.models import Book
from book.serializers import BookSerializer

BOOK_URL = reverse("book:book-list")


def create_admin_user():
    return get_user_model().objects.create_superuser(
        email="admin@test.com",
        password="adminpass",
    )


def create_user():
    return get_user_model().objects.create_user(
        email="user@test.com",
        password="userpass",
    )


def create_book(**params):
    defaults = {
        "title": "Some book",
        "cover": "Hard",
        "inventory": 5,
        "daily_fee": "1.00"
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class PublicBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_books(self):
        create_book(title="Book 1")
        create_book(title="Book 2")

        res = self.client.get(BOOK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)

    def test_cannot_create_book_unauthenticated(self):
        payload = {
            "title": "Unauthorized",
            "cover": "HD",
            "inventory": 10,
            "daily_fee": "2.00"
        }

        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.admin = create_admin_user()
        self.client.force_authenticate(user=self.user)


    def test_user_cannot_create_book(self):
        res = self.client.post(BOOK_URL, {
            "title": "Test Book",
            "cover": "SF",
            "inventory": 3,
            "daily_fee": "1.00"
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_book(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.post(BOOK_URL, {
            "title": "Admin Book",
            "cover": "HD",
            "inventory": 4,
            "daily_fee": "1.50"
        })

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, "Admin Book")


class ResponseBookApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_book_list(self):
        create_book()

        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_book_detail(self):
        book = create_book()
        url = reverse("book:book-detail", args=[book.id])

        res = self.client.get(url)
        serializer = BookSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
