from django.db import models
from datetime import date, timedelta


def add_subscription(current, **kwargs):
    delta = timedelta(**kwargs)
    return current + delta


class User(models.Model):
    name = models.CharField(
        max_length=50
    )
    subscription_end = models.DateField(
        default=add_subscription(date.today(), weeks=2)
    )
    subscription_status = models.BooleanField(
        default=True
    )

