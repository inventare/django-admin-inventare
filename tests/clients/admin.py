from django.contrib import admin
from inventare.admin_template.admin import ModelAdmin
from .models import Client

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_filter = ['is_usable']
    list_display = ['id', 'name', 'is_usable']
    list_display_links = ['id']
    list_editable = ['name', 'is_usable']
    search_fields = ['name']
