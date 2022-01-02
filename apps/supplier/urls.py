from django.urls import path

from . import views
from apps import supplier

urlpatterns = [
    path("suppliers", views.supplier_read_all, name="supplier-read-all-page"),
    path("supplier/create", views.supplier_create, name="supplier-create-page"),
    path("suppliers/<slug:slug>/update", views.supplier_update, name="supplier-update-page"),
    path("suppliers/<slug:slug>/delete", views.supplier_delete, name="supplier-delete-page")
]

# urlpatterns = [
#     path("suppliers", views.suppliers, name="supplier-read-all-page"),
#     path("supplier/create", views.supplier_create, name="supplier-create-page"),
#     path("suppliers/<slug:slug>/update", views.supplier_update, name="supplier-update-page")
# ]
