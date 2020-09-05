from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    Sum,
)

from django.test import TestCase
from .models import (
    Stock,
    Transaction
)

# Create your tests here.


class StockTestCase(TestCase):
    def setUp(self):
        Stock.objects.create(name='AREIT', price=80.21)

    def test_stock(self):
        stock = Stock.objects.get(name='AREIT')
        self.assertEqual(stock.name, 'AREIT')
        self.assertEqual(stock.price, Decimal('80.21'))


class TransactionTestCase(TestCase):
    def setUp(self):
        stock = Stock.objects.create(name='AREIT', price=80.21)
        self.user = User.objects.create_user(username='martin', email='martin@test.com', password='top_secret')

        Transaction.objects.create(
            transaction_type='buy',
            status='confirmed',
            quantity=54,
            stock=stock,
            user=self.user,
            current_price=stock.price
        )

        stock_2 = Stock.objects.get(name='AREIT')
        stock_2.price = 70.23
        stock_2.save()

        Transaction.objects.create(
            transaction_type='buy',
            status='confirmed',
            quantity=32,
            stock=stock_2,
            user=self.user,
            current_price=stock.price
        )

    def test_transaction(self):
        total_value = self.user.transactions.filter(
            stock__name='AREIT',
            transaction_type='buy').aggregate(
                sum=ExpressionWrapper(Sum(F('current_price') * F('quantity')), output_field=DecimalField()))['sum']
        self.assertEqual(total_value, Decimal('6898.06'))
