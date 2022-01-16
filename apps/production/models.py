from django.db import models
from django.core.validators import MaxLengthValidator
from apps.supplier.models import Supplier
from apps.recipe.models import Recipe

class Production(models.Model):
    datetime = models.DateField(db_index=True)
    notes = models.TextField(validators=[MaxLengthValidator(255)], blank=True)
    production_recipes = models.ManyToManyField(Recipe, through='ProductionRecipe')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PK: {self.pk}, datetime={self.datetime}"

# https://docs.djangoproject.com/en/dev/topics/db/models/#extra-fields-on-many-to-many-relationships
class ProductionRecipe(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=20, decimal_places=3)