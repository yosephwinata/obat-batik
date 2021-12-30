from django.contrib import admin

from apps.supplier.models import Supplier
from .models import Purchase

# Register your models here.

class PurchaseAdmin(admin.ModelAdmin):
    list_filter = ("datetime", "supplier")
    list_display = ("datetime", "invoice_number", "supplier", "notes", "updated_at")

admin.site.register(Purchase, PurchaseAdmin)