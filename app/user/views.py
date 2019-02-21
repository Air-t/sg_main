from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib import messages


def goto(request):
    return redirect('accounts/login/')


def home_view(request):
    return render(request, 'home.html')


def signup_view(request):
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
    if request.method == "POST":
        logout(request)
        return redirect('user:home')


@login_required(redirect_field_name='next')
def exams_view(request):
    return render(request, 'exams.html')
