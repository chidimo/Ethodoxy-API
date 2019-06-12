from django.core.management.base import BaseCommand#, CommandError

import django
from django.conf import settings

from bible.models import Version, Book
from commentary.models import Commentary, CommentaryText

from helpers.paths import COMMENTARIES

def clean_name(name):
    """Remove asterisk"""
    name = name.replace("*", "").strip().lower()
    return name

class Command(BaseCommand):
    help = 'Create New Testament Books'

    def handle(self, *args, **options):


        for each in COMMENTARIES:
            with open(each, "r+") as rh:
                commentary_file = json.load(rh)

            version, _ = Version.objects.get_or_create(name="douay-rheims")
            commentary, _ = Commentary.objects.get_or_create(name="challoner", version=version)

            for book_chapter, comment_dictionary in commentary_file.items():
                bcn = book_chapter.split("__")
                book_name = bcn[0]
                chapter = bcn[1].lstrip().rstrip()

                if " or " in book_name:
                    book_name = book_name.split(" or ")[0]

                book_name = clean_name(book_name)
                book = Book.objects.get(name=book_name)

                for verse_heading, text in comment_dictionary.items():
                    vhg = verse_heading.split("__")
                    verse = vhg[0]
                    heading = vhg[1]

                    commtext = CommentaryText.objects.get_or_create(
                        commentary=commentary, heading=heading, book=book,
                        chapter=chapter, verse=verse, text=text)

