import json

import django
from django.core.management.base import BaseCommand#, CommandError

from bible.models import Version, Book
from helpers.paths import OT

def clean_name(name):
    """Remove asterisk"""
    name = name.replace("*", "").strip().lower()
    return name

class Command(BaseCommand):
    help = 'Create Old Testament Books'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating OT books'))   
        version, _ = Version.objects.get_or_create(name="douay-rheims")
        with open(OT, "r+") as rh:
            booking = json.load(rh)

        for name, value in booking.items():
            book, _ = Book.objects.get_or_create(version=version, name=clean_name(name), testament="old testament", position=int(value[1][:2]), location=value[0])

            if "*" in name:
                book.deutero = True

            if " or " in name:
                both_names = name.split(" or ")
                book.name = clean_name(both_names[0])
                book.alt_name = clean_name(both_names[1])
            book.save(update_fields=['name', 'deutero', 'alt_name'])
        self.stdout.write(self.style.SUCCESS(f'Old Testament books created successfully'))
