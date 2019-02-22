import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'


class Command(BaseCommand):
    """Django command to create main main groups and sets up
    required permissions"""
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="owner")
        if created:
            group.name = "owner"
            group.save()

        group, created = Group.objects.get_or_create(name="student")
        if created:
            group.name = "student"
            group.save()
