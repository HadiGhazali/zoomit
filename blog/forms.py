from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=150, required=True)
    email = forms.EmailField(label=_('Email'), help_text=_('a valid email for reset your password'), required=True)
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(label=_('First name'), required=True, max_length=150)
    last_name = forms.CharField(label=_('Last name'), required=True, max_length=150)

    def clean(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)
        if password != password2:
            raise ValidationError(
                "Repeated password is false"
            )

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        return password
