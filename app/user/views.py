from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from .forms import UserCreationForm, UserChangeForm


def goto(request):
    """Redirects client to the login page."""
    return redirect('user:home')


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


@login_required()
def user_view(request):
    """Render user view"""
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'password':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Fields updated.")
                return redirect('user:user')
            else:
                messages.warning(request, 'Update failed.')
        elif action == 'profile':
            form = UserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Fields updated.")
                return redirect('user:user')
            else:
                messages.warning(request, 'Update failed.')

    profile_form = UserChangeForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    return render(request, 'user.html', {'password_form': password_form, 'profile_form': profile_form})