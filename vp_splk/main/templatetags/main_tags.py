from django import template
import main.views as views
from main.models import Supply

register = template.Library()


@register.inclusion_tag('main/includes/slider_recent_supplies.html')
def show_supplies():
    supplies_db = Supply.active.all()
    return {'supplies': supplies_db}


@register.inclusion_tag('main/includes/slider_recent_supplies.html')
def show_recent_supplies():
    supplies_db = Supply.active.all()[:4]
    return {'supplies': supplies_db}


@register.inclusion_tag('main/includes/nav_panel.html')
def show_menu():
    return {'menu': views.menu}

