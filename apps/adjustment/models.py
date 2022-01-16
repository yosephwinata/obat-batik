from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils.text import slugify

from apps.ingredient.models import Ingredient

class Adjustment(models.Model):
    datetime = models.DateField(db_index=True)
    notes = models.TextField(validators=[MaxLengthValidator(255)], blank=True)
    adjustment_ingredients = models.ManyToManyField(Ingredient, through='AdjustmentIngredient')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AdjustmentIngredient(models.Model):
    adjustment = models.ForeignKey(Adjustment, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=20, decimal_places=3)