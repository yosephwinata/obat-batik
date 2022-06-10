from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required

from .models import Purchase, PurchaseIngredient, Ingredient
from .forms import PurchaseForm

many_to_many_rows = 15

@login_required(login_url="/login/")
def purchase_read_all(request):
    context = {}

    load_template = 'purchase-read-all.html'
    context['segment'] = load_template
    context['purchases'] = Purchase.objects.all().order_by('-datetime')
    context['count'] = Purchase.objects.count()
    return render(request, 'purchase/' + load_template, context)

@login_required(login_url="/login/")
def purchase_create(request):
    context = {}
    ingredients = list(Ingredient.objects.all().values_list('name', flat=True).order_by('name'))
    many_to_many_data_list = []

    if request.method == 'POST':
        form = PurchaseForm(request.POST)

        if form.is_valid():
            purchase = Purchase(
                datetime=form.cleaned_data['datetime'],
                invoice_number=form.cleaned_data['invoice_number'],
                supplier=form.cleaned_data['supplier'],
                notes=form.cleaned_data['notes'])
            # purchase.save()

            for i in range(many_to_many_rows):
                ingredient = request.POST.get(f'ingredient-{i}')
                quantity = request.POST.get(f'quantity-{i}')
                if ingredient and quantity:
                    ingredient_obj = get_object_or_404(Ingredient, name=ingredient)
                    many_to_many_data_list.append(PurchaseIngredient(purchase=purchase, ingredient=ingredient_obj, quantity=Decimal(quantity)))

            with transaction.atomic():
                purchase.save()
                for i in many_to_many_data_list:
                    i.save()

            return HttpResponseRedirect("/purchases")

    else:
        form = PurchaseForm()

    load_template = 'purchase-create.html'
    context['form'] = form
    context['segment'] = load_template
    context['ingredients'] = ingredients
    context['range'] = range(many_to_many_rows)
    return render(request, 'purchase/' + load_template, context)

@login_required(login_url="/login/")
def purchase_update(request, pk):
    context = {}
    ingredients = list(Ingredient.objects.all().values_list('name', flat=True).order_by('name'))
    previous_many_to_many_data_list = []
    many_to_many_data_list = []
    counter = 0

    obj = get_object_or_404(Purchase, pk = pk)
    form = PurchaseForm(request.POST or None, instance = obj)

    for purchase_ingredient in PurchaseIngredient.objects.filter(purchase__pk=pk):
        previous_many_to_many_data_list.append({
            'idx': counter,
            'ingredient': purchase_ingredient.ingredient.name,
            'quantity': purchase_ingredient.quantity
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
                many_to_many_data_list.append(PurchaseIngredient(purchase=obj, ingredient=ingredient_obj, quantity=Decimal(quantity)))

        with transaction.atomic():
            form.save()
            obj.purchase_ingredients.clear()
            for i in many_to_many_data_list:
                i.save()
        return HttpResponseRedirect("/purchases")

    load_template = 'purchase-update.html'
    context['form'] = form
    context['segment'] = load_template
    context['ingredients'] = ingredients
    context['range'] = range(many_to_many_rows)
    context['purchase_ingredient'] = previous_many_to_many_data_list
    return render(request, 'purchase/' + load_template, context)

@login_required(login_url="/login/")
def purchase_delete(request, pk):
    context ={}

    obj = get_object_or_404(Purchase, pk=pk)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/purchases")

    load_template = 'purchase-delete.html'
    context['purchase'] = obj
    context['segment'] = load_template
    return render(request, 'purchase/' + load_template, context)

# def purchase_update(request, pk):
#     context = {}

#     obj = get_object_or_404(Purchase, pk = pk)
#     form = PurchaseForm(request.POST or None, instance = obj)

#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect("/purchases")

#     load_template = 'purchase-update.html'
#     context["form"] = form
#     context['segment'] = load_template
#     return render(request, 'purchase/' + load_template, context)


# def purchase_create(request):
#     context = {}

#     if request.method == 'POST':
#         form = PurchaseForm(request.POST)

#         if form.is_valid():
#             purchase = Purchase(
#                 datetime=form.cleaned_data['datetime'],
#                 invoice_number=form.cleaned_data['invoice_number'],
#                 supplier=form.cleaned_data['supplier'],
#                 notes=form.cleaned_data['notes'])
#             purchase.save()

#             return HttpResponseRedirect("/purchases")

#     else:
#         form = PurchaseForm()

#     load_template = 'purchase-create.html'
#     context['form'] = form
#     context['segment'] = load_template
#     return render(request, 'purchase/' + load_template, context)