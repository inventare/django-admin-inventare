from django.contrib import admin
from inventare.admin_template.admin import ModelAdmin
from .models import Client, Address

@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ['id', 'street']
    search_fields = ['street']

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_filter = ['is_usable', 'address']
    list_display = ['id', 'name', 'is_usable']
    list_display_links = ['id']
    list_editable = ['name', 'is_usable']
    search_fields = ['name']
    date_hierarchy = 'birth_date'
