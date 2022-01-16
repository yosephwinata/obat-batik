from django.urls import path

from . import views

urlpatterns = [
    path("adjustments", views.adjustment_read_all, name="adjustment-read-all-page"),
    path("adjustment/create", views.adjustment_create, name="adjustment-create-page"),
    path("adjustments/<int:pk>/update", views.adjustment_update, name="adjustment-update-page"),
    path("adjustments/<int:pk>/delete", views.adjustment_delete, name="adjustment-delete-page")
]