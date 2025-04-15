from django.contrib import admin
from inventare.admin_template.admin import ModelAdmin
from .models import City, Region, State

@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']

@admin.register(State)
class StateAdmin(ModelAdmin):
    list_display = ['id', 'code', 'name', 'acronym', 'region']
    list_display_links = ['id', 'code', 'name', 'acronym', 'region']
    search_fields = ['name', 'acronym']
    list_filter = ['region']

@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ['id', 'name', 'code', 'state']
    list_display_links = ['id', 'name', 'code', 'state']
    search_fields = ['name']
    list_filter = ['state', 'state__region']
