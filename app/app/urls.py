from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from core.views import FeedbackView

from user.views import goto

urlpatterns = [
    path('', goto, name='goto'),
    path('ad/', admin.site.urls),
    path('accounts/', include('user.urls')),
    path('exams/', include('core.urls')),

    path('info/about/', TemplateView.as_view(template_name='core/info/about.html'), name='about'),
    path('info/contact/', TemplateView.as_view(template_name='core/info/contact.html'), name='contact'),
    path('info/leave-feedback/', FeedbackView.as_view(), name='feedback'),
]



