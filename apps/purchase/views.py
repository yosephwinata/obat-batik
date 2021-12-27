from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def purchase(request):
    context = {}
    load_template = request.path.split('/')[-1]
    context['segment'] = load_template
    html_template = loader.get_template('purchase/' + load_template)
    return HttpResponse(html_template.render(context, request))

    # return render(request, "purchase/purchase.html", {
    #     "gondrong": "gondrong1"
    # })