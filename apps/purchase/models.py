from django.db import models
from django.core.validators import MaxLengthValidator
from apps.supplier.models import Supplier

# Create your models here.

class Purchase(models.Model):
    datetime = models.DateField(db_index=True)
    invoice_number = models.CharField(max_length=70, blank=True, db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True, db_index=True, related_name='purchases')
    notes = models.TextField(validators=[MaxLengthValidator(255)], blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PK: {self.pk}, datetime={self.datetime}, invoice_number={self.invoice_number}"