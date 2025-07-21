from django.contrib.auth import get_user_model
from django.db import models


class CoverType(models.TextChoices):
    HARD = "HD", "Hard"
    SOFT = "ST", "Soft"


class Book(models.Model):
    title = models.CharField(unique=True, null=False, max_length=255)
    # author = models.ManyToManyField("Author", related_name="books") to do
    cover = models.CharField(
        max_length=2,
        choices=CoverType.choices,
    )
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(null=False)
    expected_return_date = models.DateTimeField(null=False)
    actual_return_date = models.DateTimeField(null=True, blank=True)

    book = models.ForeignKey(
        "Book", on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="borrowings"
    )
