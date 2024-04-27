from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path("supplies/", views.supplies, name='supplies'),
    path("supplies/<int:supply_id>", views.supply, name='supply'),
    path("profile/", views.profile, name='profile'),
    path("new_supply/", views.new_supply, name='new_supply'),
    path("notifications/", views.notifications, name='notifications'),
]
