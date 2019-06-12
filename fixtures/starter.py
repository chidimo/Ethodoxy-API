"""docstring"""

import os
import json
import glob
from drb.models import (Version, Book, Chapter, Verse, Commentary, CommentaryText)

import django
from django.conf import settings
from django.db import IntegrityError

from siteuser.models import CustomUser

from council.models import Council, Category, Document, Chapter, Article

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_path = os.path.join(BASE_DIR, "drbo_org_scrap")
data_store = os.path.join(BASE_DIR, "drbo_data")
chapter_store = os.path.join(BASE_DIR, "drbo_data", "chapters")
verse_store = os.path.join(BASE_DIR, "drbo_data", "verses")
challoner_store = os.path.join(BASE_DIR, "drbo_data", "challoner")

NT = (os.path.join(data_store, "new_test.json"))
OT = (os.path.join(data_store, "old_test.json"))
CHAPS = glob.glob("{}/*.json".format(chapter_store))
VERSES = glob.glob("{}/*.json".format(verse_store))
COMMENTARIES = glob.glob("{}/*.json".format(challoner_store))

# Constitutions
#     Dei Verbum
#     Lumen Gentium
#     Sacrosanctum Concilium
#     Gaudium et Spes

# Declarations
#     Gravissimum Educationis
#     Nostra Aetate
#     Dignitatis Humanae

# Decrees
#     Ad Gentes
#     Presbyterorum Ordinis
#     Apostolicam Actuositatem
#     Optatam Totius
#     Perfectae Caritatis
#     Christus Dominus
#     Unitatis Redintegratio
#     Orientalium Ecclesiarum
#     Inter Mirifica

def setup_council():
    Council.objects.get_or_create(name='second vatican')
    for each in ['constitution', 'declaration', 'decree']:
        Category.objects.get_or_create(name=each)

def clean_name(name):
    """Remove asterisk"""
    name = name.replace("*", "").strip().lower()
    return name

def create_old_testament_books():
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

def create_new_testament_books():
    version, _ = Version.objects.get_or_create(name="douay-rheims")
    with open(NT, "r+") as rh:
        booking = json.load(rh)
    for name, value in booking.items():
        Book.objects.get_or_create(version=version, name=clean_name(name), testament="new testament", position=int(value[1][:2]), location=value[0])

def create_chapters_for_all_books():
    for each_book in CHAPS:
        with open(each_book, "r+") as rh:
            chapters_dictionary = json.load(rh)

        for name, number_and_location_dict in chapters_dictionary.items():
            if " or " in name:
                name = name.split(" or ")[0]
            book_object, _ = Book.objects.get_or_create(name=clean_name(name))

            for number, location in number_and_location_dict.items():
                Chapter.objects.create(book=book_object, number=int(number), location=location)

def create_verse_for_all_books():
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

def create_all_commentaries():
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

def setup_drb():
    create_old_testament_books()
    create_new_testament_books()
    create_chapters_for_all_books()
    create_verse_for_all_books()

def setup_challoner():
    create_all_commentaries()

if __name__ == "__main__":
    pass
    # create_chapters_for_all_books(CHAPS)
    # create_verse_for_all_books(VERSES)
    # create_all_commentaries(COMMENTARIES)
