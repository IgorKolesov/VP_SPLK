from django import template
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
def show_menu():
    return {'menu': views.menu}


@register.inclusion_tag('main/includes/cargos.html')
def show_cargos(supply_id: int):
    cargo_db = Cargo.objects.filter(supply=supply_id)
    return {'supply_id': supply_id,
            'cargos': cargo_db}


@register.inclusion_tag('main/includes/supply_chains.html')
def show_chains(supply_id: int):
    chain_db = SupplyChain.objects.filter(supply=supply_id)
    return {'supply_id': supply_id,
            'supply_chains': chain_db}


@register.inclusion_tag('main/includes/supply_files.html')
def show_files(supply_id: int):
    files_db = UploadFiles.objects.filter(supply=supply_id, supply_chain_id=None)
    return {'supply_id': supply_id,
            'supply_files': files_db}
