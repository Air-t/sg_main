from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


app_name = 'core'


def in_owner_group(user):
    if user:
        return user.groups.filter(name='owner').count() != 0
    return False


@user_passes_test(in_owner_group, login_url='user:login')
@login_required(redirect_field_name='next')
def exams_view(request):
    return render(request, 'exams.html')
