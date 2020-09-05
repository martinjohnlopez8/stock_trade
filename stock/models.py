from django.contrib.auth.models import User
from django.db import models

from trading_app.models import BaseModel

# Create your models here.


class Stock(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name


# class Portfolio(BaseModel):
#     stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Transaction(BaseModel):
    TRANSACTION_TYPE_CHOICES = (
        ('buy', 'Buy'),
        ('sell', 'Sell')
    )

    STATUS_CHOICES = (
        ('placed', 'Placed'),
        ('approved', 'Approved'),
    )

    transaction_type = models.CharField(max_length=32, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='placed')
    stock = models.ForeignKey(Stock, related_name='transactions', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.SET_NULL, null=True)
    current_price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField()
