from django.contrib import admin
from django.contrib.auth import admin as default_admin
from django.contrib.auth.models import User, Group
from inventare.admin_template.admin.htmx import HTMXModelAdminMixin

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(HTMXModelAdminMixin, default_admin.UserAdmin):
    def get_urls(self):
        return self.get_htmx_urls() + super().get_urls()

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(HTMXModelAdminMixin, default_admin.GroupAdmin):
    def get_urls(self):
        return self.get_htmx_urls() + super().get_urls()
