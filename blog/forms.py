from django import forms
from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from blog.models import Comment
# from blog.validators import validate_password, validate_username, validate_user_and_name

User = get_user_model()


# class UserRegistrationForm1(forms.Form):
#     username = forms.CharField(label=_('Username'), max_length=150, required=True,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label=_('Email'), help_text=_('a valid email for reset your password'), required=True,
#                              widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#                                required=True)
#     password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#                                 required=True)
#     first_name = forms.CharField(label=_('First name'), required=True, max_length=150,
#                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(label=_('Last name'), required=True, max_length=150,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#
#     def clean(self):
#         password = self.cleaned_data.get('password', None)
#         password2 = self.cleaned_data.get('password2', None)
#         if password != password2:
#             raise ValidationError(
#                 _("password don't match"),
#                 code='invalid'
#             )
#
#     def clean_username(self):
#         username = self.cleaned_data.get('username', None)
#         validate_username(username)
#         return username
#
#     def clean_password(self):
#         password = self.cleaned_data.get('password', None)
#         validate_password(password)
#         return password


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {'content': _('Comment'), }
        help_texts = {
            'content': _('inter your comment.'),
        }
