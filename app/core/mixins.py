from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


def is_in_owner_group(user):
    """Check if logged user is in owner Group"""
    if user.is_anonymous:
        return False
    return user.is_teacher

def is_in_student_group(user):
    """Check if logged user is in owner Group"""
    if user.is_anonymous:
        return False
    return user.is_student


class LoginRequiredOwnerMixin(AccessMixin):
    def get_login_url(self):
        if self.request.user:
            return super(LoginRequiredOwnerMixin, self).get_login_url()
        return redirect('core:exams')

    def test_func(self):
        return is_in_owner_group(self.request.user)


class LoginRequiredStudentMixin(AccessMixin):
    def get_login_url(self):
        if self.request.user:
            return super(LoginRequiredStudentMixin, self).get_login_url()
        return redirect('core:student')

    def test_func(self):
        return is_in_student_group(self.request.user)
