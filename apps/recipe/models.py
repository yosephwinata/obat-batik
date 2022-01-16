from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils.text import slugify

from apps.ingredient.models import Ingredient

class Recipe(models.Model):
    name = models.CharField(unique=True, max_length=70, db_index=True)
    notes = models.TextField(validators=[MaxLengthValidator(255)], blank=True)
    recipe_ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=20, decimal_places=3)