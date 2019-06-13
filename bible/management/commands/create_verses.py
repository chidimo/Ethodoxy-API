import json

import django
from django.conf import settings
from django.core.management.base import BaseCommand#, CommandError

from bible.models import Book, Chapter, Verse
from helpers.paths import VERSES

def clean_name(name):
    """Remove asterisk"""
    name = name.replace("*", "").strip().lower()
    return name

class Command(BaseCommand):
    help = 'Create book verses'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating Verses'))
        for each in VERSES:
            with open(each, "r+") as rh:
                verses = json.load(rh)

            for verse_chapter, chapter_text_dict in verses.items():
                parts = verse_chapter.split("__")
                book_name = parts[0]
                chapter_number = parts[1].lstrip().rstrip()

                if " or " in book_name:
                    book_name = clean_name(book_name.split(" or ")[0])
                else:
                    book_name = clean_name(book_name)

                book = Book.objects.get(name=book_name)
                chapter = Chapter.objects.get(book__name=book_name, number=chapter_number)

                for number, text in chapter_text_dict.items():
                    Verse.objects.create(chapter=chapter, number=number, text=text.strip())
        self.stdout.write(self.style.SUCCESS(f'Verses created successfully'))
