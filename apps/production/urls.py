from django.urls import path

from . import views

urlpatterns = [
    path("productions", views.production_read_all, name="production-read-all-page"),
    path("production/create", views.production_create, name="production-create-page"),
    path("productions/<int:pk>/update", views.production_update, name="production-update-page"),
    path("productions/<int:pk>/delete", views.production_delete, name="production-delete-page")
]