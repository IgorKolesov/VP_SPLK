from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path("supplies/", views.supplies, name='supplies'),
    path("supplies/<int:supply_id>/", views.supply, name='supply'),
    path("supplies/<int:supply_id>/<int:cargo_id>/", views.cargo, name='cargo'),
    path("profile/", views.profile, name='profile'),
    path("add_supply/", views.add_supply, name='add_supply'),
    path("supplies/<int:supply_id>/add_cargo/", views.add_supply, name='add_cargo'),
    path("notifications/", views.notifications, name='notifications'),
]
