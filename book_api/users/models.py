from django.db import models
from datetime import date, timedelta


class Account(models.Model):
    name = models.CharField(
        max_length=50
    )
    birthday = models.DateField(
        default=date(year=1970, month=1, day=1)
    )
    subscription_end = models.DateField(
        default=date.today() + timedelta(weeks=2)
    )

    def subscription_is_active(self):
        return self.subscription_end >= date.today()
