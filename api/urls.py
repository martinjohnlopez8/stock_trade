from django.urls import path, include

import stock.urls

urlpatterns = [
    path('stock/', include(stock.urls, namespace='stock')),
]
