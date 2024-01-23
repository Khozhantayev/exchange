from django.db import models


class CurrencyRate(models.Model):
    rate = models.FloatField()
    time_rate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rate} ({self.time_rate})'