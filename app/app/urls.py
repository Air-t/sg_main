from django.contrib import admin
from django.urls import path, include

from user.views import goto

urlpatterns = [
    path('', goto, name='goto'),
    path('admin/', admin.site.urls),
    path('accounts/', include('user.urls')),
    path('exams/', include('core.urls')),
]
