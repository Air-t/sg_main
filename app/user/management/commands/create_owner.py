import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'


class Command(BaseCommand):
    """Django command to create owner user and set its group to owner"""


    # TODO add arg handler
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(self, username, password, *args, **options):
        if username is None:
            username = options['username']
        if password is None:
            password = options['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()

        user = User.objects.get(username=username)
        group = Group.objects.get(name='owner')
        group.user_set.add(user)
        group.save()

