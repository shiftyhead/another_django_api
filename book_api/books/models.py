from django.db import models


class Book(models.Model):
    title = models.CharField(
        max_length=50
    )
    text = models.TextField()
    author = models.CharField(
        max_length=50
    )
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.title
