from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from account.validators import validate_user_and_name, validate_username, validate_password, validate_phone_number

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(label=_('Email'), max_length=150, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=True)

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        validate_user_and_name(email, password)


class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'phone_number')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)
        if password != password2:
            raise ValidationError(
                _("password don't match"),
                code='invalid'
            )
        validate_phone_number(self.cleaned_data['phone_number'])

    def clean_username(self):
        username = self.cleaned_data.get('email', None)
        validate_username(username)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        validate_password(password)
        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number[0:3] == '098':
            phone_number = '09' + phone_number.split('098')[1]
        if phone_number[0:3] == '+98':
            phone_number = '09' + phone_number.split('+98')[1]
        print(phone_number)
        return phone_number
