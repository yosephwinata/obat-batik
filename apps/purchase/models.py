from django.db import models
from apps.supplier.models import Supplier

# Create your models here.

class Purchase(models.Model):
    datetime = models.DateTimeField()
    invoice_number = models.CharField(max_length=70)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchases')
    notes = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)