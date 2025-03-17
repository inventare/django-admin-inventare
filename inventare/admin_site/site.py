from functools import update_wrapper
from django.urls import path
from django.contrib import admin
from django.urls.resolvers import URLResolver
from inventare.admin_site.views import HTMXAutocompleteView
from .forms import AuthenticationForm

class AdminSite(admin.AdminSite):
    login_form = AuthenticationForm

    def get_urls(self) -> list[URLResolver]:
        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)

            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        return [
            path("htmx/autocomplete/", wrap(self.autocomplete_view), name="htmx-autocomplete"),
        ] + super().get_urls()

    def autocomplete_view(self, request):
        return HTMXAutocompleteView.as_view(admin_site=self)(request)
    