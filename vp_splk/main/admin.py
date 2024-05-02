from django.contrib import admin

from .models import Supply


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create', 'is_active')
    list_display_links = ('id', 'name')
    ordering = ['-time_create', 'name']
