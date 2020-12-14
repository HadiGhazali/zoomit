from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from account.forms import LoginForm, UserRegistrationForm


def login_view(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('posts_archive')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        form.is_valid()
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        print(form.errors)
        user = authenticate(request, email=email, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('posts_archive')
        else:
            pass
    context = {'forms': form}
    return render(request, 'blog/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('posts_archive')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
            user = form.save(commit=False)
            password = user.password
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            pass
        context = {'form': form}
    else:
        form = UserRegistrationForm()
        context = {'form': form}
    return render(request, 'blog/register.html', context)

# Create your views here.
