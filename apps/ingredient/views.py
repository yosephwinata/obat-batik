from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from decimal import *

from apps.recipe.models import RecipeIngredient

from .models import Ingredient
from apps.purchase.models import PurchaseIngredient
from apps.production.models import ProductionRecipe
from apps.adjustment.models import AdjustmentIngredient
from .forms import IngredientForm

TYPE_PURCHASE = 'PURCHASE'
TYPE_PRODUCTION = 'PRODUCTION'
TYPE_ADJUSTMENT = 'ADJUSTMENT'

@login_required(login_url="/login/")
def ingredient_read_all(request):
    context = {}
    
    load_template = 'ingredient-read-all.html'
    context['segment'] = load_template
    context['ingredients'] = Ingredient.objects.all().order_by('name')
    context['count'] = Ingredient.objects.count()
    return render(request, 'ingredient/' + load_template, context)

@login_required(login_url="/login/")
def ingredient_create(request):
    context = {}

    if request.method == 'POST':
        form = IngredientForm(request.POST)

        if form.is_valid():
            ingredient = Ingredient(
                name=form.cleaned_data['name'])
            ingredient.save()
            return HttpResponseRedirect("/ingredients")

    else:
        form = IngredientForm()

    load_template = 'ingredient-create.html'
    context['form'] = form
    context['segment'] = load_template
    return render(request, 'ingredient/' + load_template, context)

@login_required(login_url="/login/")
def ingredient_read(request, slug):
    context = {}
    history = []

    obj = get_object_or_404(Ingredient, slug=slug)

    for adjustment_ingredient in AdjustmentIngredient.objects.filter(ingredient__slug=slug):
        history.append({
            'type': TYPE_ADJUSTMENT,
            'inventory_changes_value': adjustment_ingredient.quantity,
            'datetime': adjustment_ingredient.adjustment.datetime,
            'detail': f'[Stok Opname] {adjustment_ingredient.adjustment.notes}',
            'inventory_changes': f'{adjustment_ingredient.quantity.normalize():f}',
            'current_inventory': ''
        })

    recipe_slugs = [] # Recipes that contain the selected ingredient
    for recipe_ingredient in RecipeIngredient.objects.filter(ingredient__slug=slug):
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
                'detail': f'[Produksi] {production_recipe.recipe.name} ({production_recipe.quantity.normalize():f} resep)',
                'inventory_changes': f'-{inventory_changes.normalize():f}',
                'current_inventory': ''
        })

    for purchase_ingredient in PurchaseIngredient.objects.filter(ingredient__slug=slug):
        history.append({
            'type': TYPE_PURCHASE,
            'inventory_changes_value': purchase_ingredient.quantity,
            'datetime': purchase_ingredient.purchase.datetime,
            'detail': f'[Pembelian] {purchase_ingredient.purchase.supplier.name}',
            'inventory_changes': f'+{purchase_ingredient.quantity.normalize():f}',
            'current_inventory': ''
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
        h['current_inventory'] = f'{temp_inventory.normalize():f}'

        # print(h['type'], h['inventory_changes_value'], temp_inventory)

    load_template = 'ingredient-read.html'
    context['ingredient'] = obj
    context['history'] = history
    context['segment'] = load_template
    return render(request, 'ingredient/' + load_template, context)

@login_required(login_url="/login/")
def ingredient_update(request, slug):
    context ={}
 
    obj = get_object_or_404(Ingredient, slug = slug)
    form = IngredientForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/ingredients")
 
    load_template = 'ingredient-update.html'
    context["form"] = form
    context['segment'] = load_template
    return render(request, 'ingredient/' + load_template, context)

@login_required(login_url="/login/")
def ingredient_delete(request, slug):
    context ={}

    obj = get_object_or_404(Ingredient, slug=slug)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/ingredients")

    load_template = 'ingredient-delete.html'
    context['ingredient'] = obj
    context['segment'] = load_template
    return render(request, 'ingredient/' + load_template, context)