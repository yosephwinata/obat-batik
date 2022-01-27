from django.db import models
from django.utils.text import slugify
from decimal import *

class Ingredient(models.Model):
    name = models.CharField(unique=True, max_length=70, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Ingredient, self).save(*args, **kwargs)

    @property
    def current_inventory(self):
        from apps.recipe.models import RecipeIngredient
        from apps.purchase.models import PurchaseIngredient
        from apps.production.models import ProductionRecipe
        from apps.adjustment.models import AdjustmentIngredient

        TYPE_PURCHASE = 'PURCHASE'
        TYPE_PRODUCTION = 'PRODUCTION'
        TYPE_ADJUSTMENT = 'ADJUSTMENT'

        history = []

        for adjustment_ingredient in AdjustmentIngredient.objects.filter(ingredient__slug=self.slug):
            history.append({
                'type': TYPE_ADJUSTMENT,
                'inventory_changes_value': adjustment_ingredient.quantity,
                'datetime': adjustment_ingredient.adjustment.datetime,
            })

        recipe_slugs = [] # Recipes that contain the selected ingredient
        for recipe_ingredient in RecipeIngredient.objects.filter(ingredient__slug=self.slug):
            recipe_slug = recipe_ingredient.recipe.slug
            if recipe_slug not in recipe_slugs:
                recipe_slugs.append({
                    'recipe_slug': recipe_slug,
                    'number_of_recipes': recipe_ingredient.quantity
                })

        for recipe_slug in recipe_slugs:
            for production_recipe in ProductionRecipe.objects.filter(recipe__slug=recipe_slug['recipe_slug']):
                inventory_changes = recipe_slug['number_of_recipes'] * production_recipe.quantity
                history.append({
                    'type': TYPE_PRODUCTION,
                    'inventory_changes_value': inventory_changes,
                    'datetime': production_recipe.production.datetime,
            })

        for purchase_ingredient in PurchaseIngredient.objects.filter(ingredient__slug=self.slug):
            history.append({
                'type': TYPE_PURCHASE,
                'inventory_changes_value': purchase_ingredient.quantity,
                'datetime': purchase_ingredient.purchase.datetime,
            })

        # Sort by date DESC
        history.sort(key=lambda item:item['datetime'], reverse=True)

        # Fill the current_inventory
        temp_inventory = Decimal(0)
        for h in reversed(history):
            if h['type'] == TYPE_PURCHASE:
                temp_inventory += h['inventory_changes_value']
            elif h['type'] == TYPE_PRODUCTION:
                temp_inventory -= h['inventory_changes_value']
            elif h['type'] == TYPE_ADJUSTMENT:
                temp_inventory = h['inventory_changes_value']
        
        return f'{temp_inventory.normalize():f}'