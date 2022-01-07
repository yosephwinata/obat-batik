# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.purchase.urls")),
    path("", include("apps.supplier.urls")),
    path("", include("apps.ingredient.urls")),
    # path("supplier", include("apps.supplier.urls")),
    path("", include("apps.home.urls")),             # UI Kits Html files
]
