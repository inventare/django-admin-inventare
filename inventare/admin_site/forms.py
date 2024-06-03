from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm

class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
