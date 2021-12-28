from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def suppliers(request):
    context = {}
    load_template = 'supplier-read-all.html'
    context['segment'] = load_template
    html_template = loader.get_template('supplier/' + load_template)
    return HttpResponse(html_template.render(context, request))

# def suppliers(request):
#     context = {}
#     # load_template = request.path.split('/')[-1]
#     load_template = request.path.split('/')[-1] + '.html'
#     context['segment'] = load_template
#     html_template = loader.get_template('supplier/' + load_template)
#     return HttpResponse(html_template.render(context, request))