from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import BaseFormView, FormView

from account.forms import LoginForm, UserRegistrationForm


class Login(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'blog/login-2.html'


class Logout(LogoutView):
    pass


class RegisterView(FormView):
    form_class = UserRegistrationForm
    success_url = '../login'
    template_name = 'blog/register.html'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        user = form.save(commit=False)
        password = user.password
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(self.get_success_url())


# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             # username = form.cleaned_data['username']
#             # first_name = form.cleaned_data['first_name']
#             # last_name = form.cleaned_data['last_name']
#             # email = form.cleaned_data['email']
#             # password = form.cleaned_data['password']
#             # user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
#             user = form.save(commit=False)
#             password = user.password
#             user.set_password(password)
#             user.save()
#             return redirect('login')
#         else:
#             pass
#         context = {'form': form}
#     else:
#         form = UserRegistrationForm()
#         context = {'form': form}
#     return render(request, 'blog/register.html', context)

# Create your views here.
