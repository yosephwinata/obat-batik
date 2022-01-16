from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required

from .models import Production, ProductionRecipe, Recipe
from .forms import ProductionForm

many_to_many_rows = 15

# @login_required
def production_read_all(request):
    context = {}
    
    load_template = 'production-read-all.html'
    context['segment'] = load_template
    context['productions'] = Production.objects.all().order_by('-datetime')
    context['count'] = Production.objects.count()
    return render(request, 'production/' + load_template, context)

# @login_required
def production_create(request):
    context = {}
    recipes = list(Recipe.objects.all().values_list('name', flat=True))
    many_to_many_data_list = []

    if request.method == 'POST':
        form = ProductionForm(request.POST)

        if form.is_valid():
            production = Production(
                datetime=form.cleaned_data['datetime'],
                notes=form.cleaned_data['notes'])

            for i in range(many_to_many_rows):
                recipe = request.POST.get(f'recipe-{i}')
                quantity = request.POST.get(f'quantity-{i}')
                if recipe and quantity:
                    recipe_obj = get_object_or_404(Recipe, name=recipe)
                    many_to_many_data_list.append(ProductionRecipe(production=production, recipe=recipe_obj, quantity=Decimal(quantity)))

            with transaction.atomic():
                production.save()
                for i in many_to_many_data_list:
                    i.save()

            return HttpResponseRedirect("/productions")

    else:
        form = ProductionForm()

    load_template = 'production-create.html'
    context['form'] = form
    context['segment'] = load_template
    context['recipes'] = recipes
    context['range'] = range(many_to_many_rows)
    return render(request, 'production/' + load_template, context)

def production_update(request, pk):
    context = {}
    recipes = list(Recipe.objects.all().values_list('name', flat=True))
    previous_many_to_many_data_list = []
    many_to_many_data_list = []
    counter = 0
 
    obj = get_object_or_404(Production, pk = pk)
    form = ProductionForm(request.POST or None, instance = obj)

    for production_recipe in ProductionRecipe.objects.filter(production__pk=pk):
        previous_many_to_many_data_list.append({
            'idx': counter,
            'recipe': production_recipe.recipe.name,
            'quantity': production_recipe.quantity
        })
        counter += 1
    # Fill the rest of the list with empty values
    for i in range(many_to_many_rows - len(previous_many_to_many_data_list)):
        previous_many_to_many_data_list.append({
            'idx': counter,
            'recipe': '',
            'quantity': None
        })
        counter += 1

    if form.is_valid():
        for i in range(many_to_many_rows):
            recipe = request.POST.get(f'recipe-{i}')
            quantity = request.POST.get(f'quantity-{i}')
            if recipe and quantity:
                recipe_obj = get_object_or_404(Recipe, name=recipe)
                many_to_many_data_list.append(ProductionRecipe(production=obj, recipe=recipe_obj, quantity=Decimal(quantity)))

        with transaction.atomic():
            form.save()
            obj.production_recipes.clear()
            for i in many_to_many_data_list:
                i.save()
        return HttpResponseRedirect("/productions")
 
    load_template = 'production-update.html'
    context['form'] = form
    context['segment'] = load_template
    context['recipes'] = recipes
    context['range'] = range(many_to_many_rows)
    context['production_recipe'] = previous_many_to_many_data_list
    return render(request, 'production/' + load_template, context)

def production_delete(request, pk):
    context ={}

    obj = get_object_or_404(Production, pk=pk)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/productions")

    load_template = 'production-delete.html'
    context['production'] = obj
    context['segment'] = load_template
    return render(request, 'production/' + load_template, context)