from django.urls import path

from . import views
from apps import supplier

urlpatterns = [
    path("suppliers", views.suppliers, name="supplier-read-all-page"),
    path("supplier/create", views.supplier_create, name="supplier-create-page"),
    path("suppliers/<str:name>/update", views.supplier_update, name="supplier-update-page")
    # path("suppliers", views.suppliers)
]

# urlpatterns = [
#     path('', views.supplier, name='supplier-page')
# ]
