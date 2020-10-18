from django.db import models
from datetime import date, timedelta


class Account(models.Model):
    name = models.CharField(
        max_length=50
    )
    birthday = models.DateField()
    subscription_end = models.DateField()

    def subscription_is_active(self):
        return self.subscription_end >= date.today()
