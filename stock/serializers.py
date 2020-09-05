from rest_framework import serializers

from .models import (
    Stock,
    Transaction
)


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'name', 'price']


class TransactionSerializer(serializers.ModelSerializer):
    stock_id = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'status', 'stock_id', 'quantity']

    def create(self, validated_data):
        ModelClass = self.Meta.model
        user = self.context['request'].user

        stock_id = validated_data.pop('stock_id')
        stock = Stock.objects.get(id=stock_id)

        transaction = ModelClass.objects.create(**validated_data, user=user, stock=stock, current_price=stock.price)

        return transaction
