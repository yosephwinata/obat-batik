from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import Supplier

# Create your views here.

def suppliers(request):
    context = {}
    load_template = 'supplier-read-all.html'
    context['segment'] = load_template
    # latest_posts = Post.objects.all().order_by("-date")[:3]
    context['suppliers'] = Supplier.objects.all()
    print('toto', context)
    return render(request, 'supplier/' + load_template, context)


##V2
# def suppliers(request):
#     context = {}
#     load_template = 'supplier-read-all.html'
#     context['segment'] = load_template
#     html_template = loader.get_template('supplier/' + load_template)
#     return HttpResponse(html_template.render(context, request))

##V1
# def suppliers(request):
#     context = {}
#     # load_template = request.path.split('/')[-1]
#     load_template = request.path.split('/')[-1] + '.html'
#     context['segment'] = load_template
#     html_template = loader.get_template('supplier/' + load_template)
#     return HttpResponse(html_template.render(context, request))