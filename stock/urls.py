from . import views

from django.urls import (
    include,
    path
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transaction', views.TransactionSetView, basename='transaction')

app_name = 'stock'

urlpatterns = [
    path('', include(router.urls)),
    path('get/', views.GetStockValueView.as_view())
]
