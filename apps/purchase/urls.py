from django.urls import path

from . import views

urlpatterns = [
    path("purchases", views.purchase_read_all, name="purchase-read-all-page"),
    path("purchase/create", views.purchase_create, name="purchase-create-page"),
    path("purchases/<int:pk>/update", views.purchase_update, name="purchase-update-page"),
    path("purchases/<int:pk>/delete", views.purchase_delete, name="purchase-delete-page")
]
