from . import serializers
from django.db.models import (
    ExpressionWrapper,
    Sum,
    F,
    DecimalField
)

from .models import (
    Transaction
)
from rest_framework import (
    permissions,
    generics,
    views,
    viewsets
)
from rest_framework.response import Response


# Create your views here.


class TransactionSetView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TransactionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request
        })
        return context

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class GetStockValueView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.StockSerializer

    def get(self, request, *args, **kwargs):
        stock_id = self.request.GET.get('stock_id', None)

        if stock_id:
            total_value = self.request.user.transactions.filter(
                stock__id=stock_id,
                transaction_type='buy'
            ).aggregate(
                sum=ExpressionWrapper(Sum(F('current_price') * F('quantity')), output_field=DecimalField())
            )['sum']
            # total_value = 0
            # print(transactions)
            # for transaction in transactions:
            #     total_value += transaction.current_price * transaction.quantity

        return Response(data={'stock_value': total_value}, status=200)
