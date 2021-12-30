from django.contrib import admin
from .models import Supplier

# Register your models here.

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at")

admin.site.register(Supplier, SupplierAdmin)