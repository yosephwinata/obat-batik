from django.urls import path

from . import views

urlpatterns = [
    path("supplier.html", views.supplier)
]
