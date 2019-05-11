from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .forms import UserCreationForm, UserChangeForm


def goto(request):
    """Redirects client to the login page."""
    return redirect('user:home')


# Pure django authentication
class SignupView(View):
    """Handles sign uo view."""

    def get(self, request, *args, **kwargs):
        return render(request, 'user/signup.html', {'form': UserCreationForm()})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "User created.")
            return redirect('user:home')
        return render(request, 'user/signup.html', {'form': form})


class LoginView(View):
    """Handles login view"""

    def get(self, request, *args, **kwargs):
        return render(request, 'user/login.html', {'form': AuthenticationForm()})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            if request.user.is_teacher:
                return redirect('core:exams')
            if request.user.is_student:
                return redirect('core:student')
            return redirect('user:home')
        messages.warning(request, 'Failed to login. Please provide valid credentials.')
        return redirect('user:login')


class LogoutView(View):
    """Loggs user out request"""

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('user:home')


class UserView(View):
    """Handles User view"""

    def get(self, request, *args, **kwargs):
        profile_form = UserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

        return render(request, 'user/user.html', {'password_form': password_form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'password':
            form = PasswordChangeForm(user=request.user, data=request.POST)
        else:
            form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Fields updated.")
            return redirect('user:user')
        else:
            messages.warning(request, 'Update failed.')

        return render(request, 'user/user.html', {'password_form': PasswordChangeForm(user=request.user),
                                                  'profile_form': UserChangeForm(instance=request.user)})


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
