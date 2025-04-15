from django.urls.resolvers import URLPattern
from django.contrib import admin
from .htmx import HTMXModelAdminMixin
from .contrib import UserAdmin

class ModelAdmin(HTMXModelAdminMixin, admin.ModelAdmin):
    # list_per_page = 2

    def get_urls(self) -> list[URLPattern]:
        return self.get_htmx_urls() + super().get_urls()


__all__ = ['HTMXModelAdminMixin', 'ModelAdmin', 'UserAdmin']
