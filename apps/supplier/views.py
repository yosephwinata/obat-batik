from django.shortcuts import get_object_or_404, render
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
    context['count'] = Supplier.objects.count()
    return render(request, 'supplier/' + load_template, context)

def supplier_create(request):
    context = {}
    load_template = 'supplier-create.html'
    context['segment'] = load_template
    return render(request, 'supplier/' + load_template, context)

def supplier_update(request, slug):
    context = {}
    load_template = 'supplier-update.html'
    context['supplier'] = get_object_or_404(Supplier, slug=slug)
    context['segment'] = load_template
    return render(request, 'supplier/' + load_template, context)


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post
#     })


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