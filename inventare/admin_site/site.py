from django.contrib import admin
from .forms import AuthenticationForm

class AdminSite(admin.AdminSite):
    login_form = AuthenticationForm
