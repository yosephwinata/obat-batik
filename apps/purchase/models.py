from django.db import models
from django.core.validators import MaxLengthValidator
from apps.supplier.models import Supplier
from apps.ingredient.models import Ingredient

class Purchase(models.Model):
    datetime = models.DateField(db_index=True)
    invoice_number = models.CharField(max_length=70, blank=True, db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True, db_index=True, related_name='purchases')
    notes = models.TextField(validators=[MaxLengthValidator(255)], blank=True)
    purchase_ingredients = models.ManyToManyField(Ingredient, through='PurchaseIngredient')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PK: {self.pk}, datetime={self.datetime}, invoice_number={self.invoice_number}"

# https://docs.djangoproject.com/en/dev/topics/db/models/#extra-fields-on-many-to-many-relationships
class PurchaseIngredient(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=20, decimal_places=3)