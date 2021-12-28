from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def purchases(request):
    context = {}
    load_template = 'purchase-read-all.html'
    context['segment'] = load_template
    html_template = loader.get_template('purchase/' + load_template)
    return HttpResponse(html_template.render(context, request))