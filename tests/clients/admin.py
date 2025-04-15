from django.contrib import admin
from inventare.admin_template.admin import ModelAdmin
from .models import Client, Address, ClientPhone

@admin.register(ClientPhone)
class ClientPhoneAdmin(ModelAdmin):
    list_display = ['id', 'client', 'phone']
    list_display_links = ['id', 'client', 'phone']

@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ['id', 'street']
    search_fields = ['street']
    ordering = ['street']

class ClientPhoneInlineAdmin(admin.TabularInline):
    model = ClientPhone
    extra = 0

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_filter = ['is_usable', 'address']
    list_display = ['id', 'name', 'is_usable']
    list_display_links = ['id']
    list_editable = ['name', 'is_usable']
    search_fields = ['name']
    date_hierarchy = 'birth_date'
    
    fieldsets = [
        ("Dados Pessoais", { 'fields': ['name', 'birth_date'], 'classes': 'cols-2' }),
        ("Sistema", { 'fields': ['is_usable'] })
    ]

    inlines = [ClientPhoneInlineAdmin]
