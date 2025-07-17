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
