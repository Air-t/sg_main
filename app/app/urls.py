from django.contrib import admin
from django.urls import path, include

from user.views import goto

urlpatterns = [
    path('', goto, name='goto'),
    path('ad/', admin.site.urls),
    path('accounts/', include('user.urls')),
    path('exams/', include('core.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
