from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path("supplies/", views.supplies, name='supplies'),
    path("supplies/<int:supply_id>/", views.supply, name='supply'),
    path("supplies/<int:supply_id>/cargo/<int:cargo_id>/", views.cargo, name='cargo'),
    path("supplies/<int:supply_id>/chain/<int:supply_chain_serial_number>/", views.supply_chain, name='supply_chain'),
    path("profile/", views.profile, name='profile'),
    path("add_supply/", views.add_supply, name='add_supply'),
    path("supplies/<int:supply_id>/add_cargo/", views.add_cargo, name='add_cargo'),
    path("supplies/<int:supply_id>/add_supply_chain/", views.add_supply_chain, name='add_supply_chain'),
    path("notifications/", views.notifications, name='notifications'),
]
