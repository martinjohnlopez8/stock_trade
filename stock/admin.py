from django.contrib import admin
from .models import (
	Stock,
	Transaction
)

# Register your models here.

admin.site.register(Stock)
admin.site.register(Transaction)
