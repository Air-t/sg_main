import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'


class Command(BaseCommand):
    """Django command to create main groups and sets up
    required permissions"""
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="teacher")
        if created:
            group.name = "teacher"
            group.save()

        group, created = Group.objects.get_or_create(name="student")
        if created:
            group.name = "student"
            group.save()
