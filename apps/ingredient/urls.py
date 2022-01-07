from django.urls import path

from . import views

urlpatterns = [
    path("ingredients", views.ingredient_read_all, name="ingredient-read-all-page"),
    path("ingredient/create", views.ingredient_create, name="ingredient-create-page"),
    path("ingredients/<slug:slug>/update", views.ingredient_update, name="ingredient-update-page"),
    path("ingredients/<slug:slug>/delete", views.ingredient_delete, name="ingredient-delete-page")
]