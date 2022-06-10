from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required

from .models import Recipe, RecipeIngredient, Ingredient
from .forms import RecipeForm

many_to_many_rows = 15

@login_required(login_url="/login/")
def recipe_read_all(request):
    context = {}

    load_template = 'recipe-read-all.html'
    context['segment'] = load_template
    context['recipes'] = Recipe.objects.all().order_by('name')
    context['count'] = Recipe.objects.count()
    return render(request, 'recipe/' + load_template, context)

@login_required(login_url="/login/")
def recipe_create(request):
    context = {}
    ingredients = list(Ingredient.objects.all().values_list('name', flat=True).order_by('name'))
    many_to_many_data_list = []

    if request.method == 'POST':
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe = Recipe(
                name=form.cleaned_data['name'],
                notes=form.cleaned_data['notes'])

            for i in range(many_to_many_rows):
                ingredient = request.POST.get(f'ingredient-{i}')
                quantity = request.POST.get(f'quantity-{i}')
                if ingredient and quantity:
                    ingredient_obj = get_object_or_404(Ingredient, name=ingredient)
                    many_to_many_data_list.append(RecipeIngredient(recipe=recipe, ingredient=ingredient_obj, quantity=Decimal(quantity)))

            with transaction.atomic():
                recipe.save()
                for i in many_to_many_data_list:
                    i.save()

            return HttpResponseRedirect("/recipes")

    else:
        form = RecipeForm()

    load_template = 'recipe-create.html'
    context['form'] = form
    context['segment'] = load_template
    context['ingredients'] = ingredients
    context['range'] = range(many_to_many_rows)
    return render(request, 'recipe/' + load_template, context)

@login_required(login_url="/login/")
def recipe_update(request, slug):
    context = {}
    ingredients = list(Ingredient.objects.all().values_list('name', flat=True).order_by('name'))
    previous_many_to_many_data_list = []
    many_to_many_data_list = []
    counter = 0

    obj = get_object_or_404(Recipe, slug = slug)
    form = RecipeForm(request.POST or None, instance = obj)

    for recipe_ingredient in RecipeIngredient.objects.filter(recipe__slug=slug):
        previous_many_to_many_data_list.append({
            'idx': counter,
            'ingredient': recipe_ingredient.ingredient.name,
            'quantity': recipe_ingredient.quantity
        })
        counter += 1
    # Fill the rest of the list with empty values
    for i in range(many_to_many_rows - len(previous_many_to_many_data_list)):
        previous_many_to_many_data_list.append({
            'idx': counter,
            'ingredient': '',
            'quantity': None
        })
        counter += 1

    if form.is_valid():
        for i in range(many_to_many_rows):
            ingredient = request.POST.get(f'ingredient-{i}')
            quantity = request.POST.get(f'quantity-{i}')
            if ingredient and quantity:
                ingredient_obj = get_object_or_404(Ingredient, name=ingredient)
                many_to_many_data_list.append(RecipeIngredient(recipe=obj, ingredient=ingredient_obj, quantity=Decimal(quantity)))

        with transaction.atomic():
            form.save()
            obj.recipe_ingredients.clear()
            for i in many_to_many_data_list:
                i.save()
        return HttpResponseRedirect("/recipes")

    load_template = 'recipe-update.html'
    context['form'] = form
    context['segment'] = load_template
    context['ingredients'] = ingredients
    context['range'] = range(many_to_many_rows)
    context['recipe_ingredient'] = previous_many_to_many_data_list
    return render(request, 'recipe/' + load_template, context)

@login_required(login_url="/login/")
def recipe_delete(request, slug):
    context ={}

    obj = get_object_or_404(Recipe, slug=slug)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/recipes")

    load_template = 'recipe-delete.html'
    context['recipe'] = obj
    context['segment'] = load_template
    return render(request, 'recipe/' + load_template, context)