from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import Supplier
from .forms import SupplierForm

# @login_required
def supplier_read_all(request):
    context = {}
    
    load_template = 'supplier-read-all.html'
    context['segment'] = load_template
    # latest_posts = Supplier.objects.all().order_by("-name")[:3]
    context['suppliers'] = Supplier.objects.all().order_by('name')
    context['count'] = Supplier.objects.count()
    return render(request, 'supplier/' + load_template, context)

# @login_required
def supplier_create(request):
    context = {}

    if request.method == 'POST':
        form = SupplierForm(request.POST)

        if form.is_valid():
            supplier = Supplier(
                name=form.cleaned_data['name'])
            supplier.save()
            return HttpResponseRedirect("/suppliers")

    else:
        form = SupplierForm()

    load_template = 'supplier-create.html'
    context['form'] = form
    context['segment'] = load_template
    return render(request, 'supplier/' + load_template, context)

def supplier_update(request, slug):
    context = {}
    load_template = 'supplier-update.html'
    context['supplier'] = get_object_or_404(Supplier, slug=slug)
    context['segment'] = load_template
    return render(request, 'supplier/' + load_template, context)

def supplier_update(request, slug):
    context ={}
 
    obj = get_object_or_404(Supplier, slug = slug)
    form = SupplierForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/suppliers")
 
    load_template = 'supplier-update.html'
    context["form"] = form
    context['segment'] = load_template
    return render(request, 'supplier/' + load_template, context)

# def supplier_update(request, slug):
#     print("REQUEST TOTO", request)
#     if request.method == 'POST':
#         form = SupplierForm(request.POST, instance=request.supplier)
#         if form.is_valid():
#             form.save()
#             # messages.success(request, f'Your account has been updated!')
#             return HttpResponseRedirect("/suppliers")
#     else:
#         form = SupplierForm(instance=request.supplier)

#     load_template = 'supplier-update.html'
#     context = {
#         'form': form,
#         'segment': load_template
#     }

#     return render(request, 'supplier/' + load_template, context)

# @login_required
def supplier_delete(request, slug):
    context ={}

    obj = get_object_or_404(Supplier, slug=slug)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/suppliers")

    load_template = 'supplier-delete.html'
    context['supplier'] = obj
    context['segment'] = load_template
    return render(request, 'supplier/' + load_template, context)