from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import DeleteView
from django.db import IntegrityError

from .models import Supplier
from .forms import SupplierForm

# Create your views here.

def supplier_read_all(request):
    context = {}
    
    load_template = 'supplier-read-all.html'
    context['segment'] = load_template
    # latest_posts = Supplier.objects.all().order_by("-name")[:3]
    context['suppliers'] = Supplier.objects.all()
    context['count'] = Supplier.objects.count()
    return render(request, 'supplier/' + load_template, context)

def supplier_create(request):
    context = {}

    if request.method == 'POST':
        form = SupplierForm(request.POST)

        if form.is_valid():
            try:
                supplier = Supplier(
                    name=form.cleaned_data['name'])
                supplier.save()
                return HttpResponseRedirect("/suppliers")
            except IntegrityError as e: 
                print(e)
                if 'UNIQUE constraint' in str(e):
                    context['error_msg'] = 'Nama sudah terdaftar'

    else:
        form = SupplierForm()

    load_template = 'supplier-create.html'
    context['segment'] = load_template
    context['form'] = form
    return render(request, 'supplier/' + load_template, context)

def supplier_update(request, slug):
    context = {}
    load_template = 'supplier-update.html'
    context['supplier'] = get_object_or_404(Supplier, slug=slug)
    context['segment'] = load_template
    return render(request, 'supplier/' + load_template, context)


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