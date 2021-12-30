from django.urls import path

from . import views

urlpatterns = [
    path("suppliers", views.suppliers, name="supplier-read-all-page")
    # path("suppliers", views.suppliers)
]

# urlpatterns = [
#     path('', views.supplier, name='supplier-page')
# ]
