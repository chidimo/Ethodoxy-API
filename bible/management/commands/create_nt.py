import json

import django
from django.core.management.base import BaseCommand#, CommandError

from bible.models import Version, Book
from helpers.paths import NT

def clean_name(name):
    """Remove asterisk"""
    name = name.replace("*", "").strip().lower()
    return name

class Command(BaseCommand):
    help = 'Create New Testament Books'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating NT books'))
        version, _ = Version.objects.get_or_create(name="douay-rheims")
        with open(NT, "r+") as rh:
            booking = json.load(rh)
        for name, value in booking.items():
            Book.objects.get_or_create(version=version, name=clean_name(name), testament="new testament", position=int(value[1][:2]), location=value[0])
        self.stdout.write(self.style.SUCCESS(f'New Testament books created successfully'))
