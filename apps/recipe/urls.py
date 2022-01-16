from django.urls import path

from . import views

urlpatterns = [
    path("recipes", views.recipe_read_all, name="recipe-read-all-page"),
    path("recipe/create", views.recipe_create, name="recipe-create-page"),
    path("recipes/<slug:slug>/update", views.recipe_update, name="recipe-update-page"),
    path("recipes/<slug:slug>/delete", views.recipe_delete, name="recipe-delete-page")
]