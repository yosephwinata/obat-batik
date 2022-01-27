from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required

from .models import Adjustment, AdjustmentIngredient, Ingredient
from .forms import AdjustmentForm

many_to_many_rows = 15

@login_required(login_url="/login/")
def adjustment_read_all(request):
    context = {}
    
    load_template = 'adjustment-read-all.html'
    context['segment'] = load_template
    context['adjustments'] = Adjustment.objects.all().order_by('-datetime')
    context['count'] = Adjustment.objects.count()
    return render(request, 'adjustment/' + load_template, context)

@login_required(login_url="/login/")
def adjustment_create(request):
    context = {}
    ingredients = list(Ingredient.objects.all().values_list('name', flat=True))
    many_to_many_data_list = []

    if request.method == 'POST':
        form = AdjustmentForm(request.POST)

        if form.is_valid():
            adjustment = Adjustment(
                datetime=form.cleaned_data['datetime'],
                notes=form.cleaned_data['notes'])

            for i in range(many_to_many_rows):
                ingredient = request.POST.get(f'ingredient-{i}')
                quantity = request.POST.get(f'quantity-{i}')
                if ingredient and quantity:
                    ingredient_obj = get_object_or_404(Ingredient, name=ingredient)
                    many_to_many_data_list.append(AdjustmentIngredient(adjustment=adjustment, ingredient=ingredient_obj, quantity=Decimal(quantity)))

            with transaction.atomic():
                adjustment.save()
                for i in many_to_many_data_list:
                    i.save()

            return HttpResponseRedirect("/adjustments")

    else:
        form = AdjustmentForm()

    load_template = 'adjustment-create.html'
    context['form'] = form
    context['segment'] = load_template
    context['ingredients'] = ingredients
    context['range'] = range(many_to_many_rows)
    return render(request, 'adjustment/' + load_template, context)

@login_required(login_url="/login/")
def adjustment_update(request, pk):
    context = {}
    ingredients = list(Ingredient.objects.all().values_list('name', flat=True))
    previous_many_to_many_data_list = []
    many_to_many_data_list = []
    counter = 0
 
    obj = get_object_or_404(Adjustment, pk = pk)
    form = AdjustmentForm(request.POST or None, instance = obj)

    for adjustment_ingredient in AdjustmentIngredient.objects.filter(adjustment__pk=pk):
        previous_many_to_many_data_list.append({
            'idx': counter,
            'ingredient': adjustment_ingredient.ingredient.name,
            'quantity': adjustment_ingredient.quantity
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
                many_to_many_data_list.append(AdjustmentIngredient(adjustment=obj, ingredient=ingredient_obj, quantity=Decimal(quantity)))

        with transaction.atomic():
            form.save()
            obj.adjustment_ingredients.clear()
            for i in many_to_many_data_list:
                i.save()
        return HttpResponseRedirect("/adjustments")
 
    load_template = 'adjustment-update.html'
    context['form'] = form
    context['segment'] = load_template
    context['ingredients'] = ingredients
    context['range'] = range(many_to_many_rows)
    context['adjustment_ingredient'] = previous_many_to_many_data_list
    return render(request, 'adjustment/' + load_template, context)

@login_required(login_url="/login/")
def adjustment_delete(request, pk):
    context ={}

    obj = get_object_or_404(Adjustment, pk=pk)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/adjustments")

    load_template = 'adjustment-delete.html'
    context['adjustment'] = obj
    context['segment'] = load_template
    return render(request, 'adjustment/' + load_template, context)