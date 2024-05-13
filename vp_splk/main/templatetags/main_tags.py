from django import template
from django.contrib.auth import get_user_model

import main.views as views
from main.models import Supply, SupplyChain, UploadFiles
from main.models import Cargo

register = template.Library()


@register.inclusion_tag('main/includes/supplies.html')
def show_supplies():
    supplies_db = Supply.active.all()
    return {'supplies': supplies_db}


@register.inclusion_tag('main/includes/supplies.html')
def show_recent_supplies():
    supplies_db = Supply.active.all()[:4]
    return {'supplies': supplies_db}


@register.inclusion_tag('main/includes/nav_panel.html')
def show_menu(user, perms):
    return {'menu': views.menu, 'user': user, 'perms': perms}


@register.inclusion_tag('main/includes/supply_cargos.html')
def show_cargos(supply_id: int, perms):
    cargo_db = Cargo.objects.filter(supply=supply_id)
    return {'supply_id': supply_id,
            'cargos': cargo_db,
            'perms': perms,
            }


@register.inclusion_tag('main/includes/supply_chains.html')
def show_chains(supply_id: int, perms):
    chain_db = SupplyChain.objects.filter(supply=supply_id)
    return {'supply_id': supply_id,
            'supply_chains': chain_db,
            'perms': perms,
            }


@register.inclusion_tag('main/includes/supply_files.html')
def show_files(supply_id: int, perms):
    files_db = UploadFiles.objects.filter(supply=supply_id, supply_chain_id=None)
    return {'supply_id': supply_id,
            'supply_files': files_db,
            'perms': perms,
            }
