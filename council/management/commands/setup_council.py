import django
from django.conf import settings
from django.core.management.base import BaseCommand#, CommandError

from council.models import Council, Category

class Command(BaseCommand):
    help = 'Create New Testament Books'

    def handle(self, *args, **options):


        Council.objects.get_or_create(name='second vatican')
        for each in ['constitution', 'declaration', 'decree']:
            Category.objects.get_or_create(name=each)
