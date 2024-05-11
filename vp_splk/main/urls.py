from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='main'),
    path("profile/", views.profile, name='profile'),
    path("notifications/", views.notifications, name='notifications'),

    path("supplies/", views.Supplies.as_view(), name='supplies'),

    path("supplies/<int:supply_id>/", views.ShowSupply.as_view(), name='supply'),
    path("supplies/<int:supply_id>/cargo/<int:cargo_id>/", views.ShowCargo.as_view(), name='cargo'),
    path("supplies/<int:supply_id>/chain/<int:supply_chain_id>/", views.ShowSupplyChain.as_view(), name='supply_chain'),

    path("add_supply/", views.AddSupply.as_view(), name='add_supply'),
    path("supplies/<int:supply_id>/add_cargo/", views.AddCargo.as_view(), name='add_cargo'),
    path("supplies/<int:supply_id>/add_supply_chain/", views.AddSupplyChain.as_view(), name='add_supply_chain'),

    path("supplies/<int:pk>/edit/", views.UpdateSupply.as_view(), name='edit_supply'),
    path("supplies/<int:supply_id>/cargo/<int:pk>/edit/", views.UpdateCargo.as_view(), name='edit_cargo'),
    path("supplies/<int:supply_id>/chain/<int:pk>/edit/", views.UpdateSupplyChain.as_view(), name='edit_chain'),

]
