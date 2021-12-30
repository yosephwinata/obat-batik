from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def purchases(request):
    context = {}
    load_template = 'purchase-read-all.html'
    context['segment'] = load_template
    return render(request, 'purchase/' + load_template, context)