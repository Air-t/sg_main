from django.urls import path

from .views import home_view, signup_view, login_view, logout_view, user_view

app_name = 'user'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/', user_view, name='user'),
]
