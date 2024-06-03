from django.contrib.admin.apps import AdminConfig


class AdminSiteConfig(AdminConfig):
    default_site = "inventare.admin_site.site.AdminSite"
