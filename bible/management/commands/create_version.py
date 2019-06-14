import json

import django
from django.core.management.base import BaseCommand

from bible.models import Version

class Command(BaseCommand):
    help = 'Create bible version'

    def add_arguments(self, parser):
        parser.add_argument('-name', type=str)
        parser.add_argument('-location', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating version'))
        name = options['name'] if options['name'] else 'douay-rheims'
        location = options['location'] if options['location'] else "http://drbo.org/"
        
        Version.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(f'{name.title()} version created successfully'))
