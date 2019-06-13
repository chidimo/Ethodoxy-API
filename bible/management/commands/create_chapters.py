import json

import django
from django.core.management.base import BaseCommand#, CommandError

from bible.models import Version, Book, Chapter, Verse
from helpers.paths import CHAPS

def clean_name(name):
    """Remove asterisk"""
    name = name.replace("*", "").strip().lower()
    return name

class Command(BaseCommand):
    help = 'Create book chapters'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating chapters'))
        for each_book in CHAPS:
            with open(each_book, "r+") as rh:
                chapters_dictionary = json.load(rh)

            for name, number_and_location_dict in chapters_dictionary.items():
                if " or " in name:
                    name = name.split(" or ")[0]
                book_object, _ = Book.objects.get_or_create(name=clean_name(name))

                for number, location in number_and_location_dict.items():
                    Chapter.objects.create(book=book_object, number=int(number), location=location)
        self.stdout.write(self.style.SUCCESS(f'Book chapters created successfully'))
