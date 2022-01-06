from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import Purchase
from .forms import PurchaseForm

# @login_required
def purchase_read_all(request):
    context = {}
    
    load_template = 'purchase-read-all.html'
    context['segment'] = load_template
    context['purchases'] = Purchase.objects.all().order_by('-datetime')
    context['count'] = Purchase.objects.count()
    return render(request, 'purchase/' + load_template, context)

# @login_required
def purchase_create(request):
    context = {}

    if request.method == 'POST':
        form = PurchaseForm(request.POST)

        if form.is_valid():
            try:
                purchase = Purchase(
                    datetime=form.cleaned_data['datetime'],
                    invoice_number=form.cleaned_data['invoice_number'],
                    supplier=form.cleaned_data['supplier'],
                    notes=form.cleaned_data['notes'])
                purchase.save()
                return HttpResponseRedirect("/purchases")
            except IntegrityError as e:
                pass
                # print(e)
                # if 'UNIQUE constraint' in str(e):
                #     context['error_msg'] = 'Nama sudah terdaftar'

    else:
        form = PurchaseForm()

    load_template = 'purchase-create.html'
    context['form'] = form
    context['segment'] = load_template
    return render(request, 'purchase/' + load_template, context)