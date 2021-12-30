from django.urls import path

from . import views

urlpatterns = [
    path("purchases", views.purchases, name="purchase-read-all-page")
]
