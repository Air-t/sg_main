from django.urls import path

from core.views import exams_view


app_name = 'core'

urlpatterns = [
    path('', exams_view, name='exams'),
]
