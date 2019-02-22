from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.contrib import messages

from .forms import UserCreationForm


def goto(request):
    """Redirects client to the login page."""
    return redirect('user:login')


def home_view(request):
    """Renders home view."""
    return render(request, 'home.html')


def signup_view(request):
    """Renders sign uo view."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "User created.")
            messages.success(request, "You are now logged in.")
            return redirect('user:home')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """Renders login view."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect('user:home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Logs user out."""
    if request.method == "POST":
        logout(request)
        return redirect('user:home')

