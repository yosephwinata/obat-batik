from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import Ingredient
from .forms import IngredientForm

# @login_required
def ingredient_read_all(request):
    context = {}
    
    load_template = 'ingredient-read-all.html'
    context['segment'] = load_template
    # latest_posts = Ingredient.objects.all().order_by("-name")[:3]
    context['ingredients'] = Ingredient.objects.all().order_by('name')
    context['count'] = Ingredient.objects.count()
    return render(request, 'ingredient/' + load_template, context)

# @login_required
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

def ingredient_update(request, slug):
    context = {}
    load_template = 'ingredient-update.html'
    context['ingredient'] = get_object_or_404(Ingredient, slug=slug)
    context['segment'] = load_template
    return render(request, 'ingredient/' + load_template, context)

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

# @login_required
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