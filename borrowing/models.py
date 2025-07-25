from django.contrib.auth import get_user_model
from django.db import models

class Borrowing(models.Model):
    borrow_date = models.DateTimeField(null=False)
    expected_return_date = models.DateTimeField(null=False)
    actual_return_date = models.DateTimeField(null=True, blank=True)

    book = models.ForeignKey(
        "book.Book", on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="borrowings"
    )
