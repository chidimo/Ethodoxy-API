"""docstring"""

import os
import json
import glob
from drb.models import (Version, Book, Chapter, Verse, Commentary, CommentaryText)

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
# print(CHAPS)
# print(VERSES)
# print(COMMENTARIES)

def clean_name(name):
    """Remove asterisk"""
    return name.replace("*", "").lstrip().rstrip()

def create_version(name="Douay-Rheims", location="http://drbo.org/"):
    Version.objects.create(name=name, location=location)

def create_old_testament_books():
    version, _ = Version.objects.get_or_create(name="Douay-Rheims")
    with open(OT, "r+") as rh:
        booking = json.load(rh)

    for name, value in booking.items():
        book = Book(
            version=version,
            name=clean_name(name),
            testament="OLD TESTAMENT",
            position=int(value[1][:2]),
            location=value[0])

        if "*" in name:
            book.deutero = True

        if " or " in name:
            both_names = name.split(" or ")
            book.name = clean_name(both_names[0])
            book.alt_name = clean_name(both_names[1])
        book.save()

def create_new_testament_books():
    version, _ = Version.objects.get_or_create(name="Douay-Rheims")
    with open(NT, "r+") as rh:
        booking = json.load(rh)
    for name, value in booking.items():
        book = Book(
            version=version,
            name=clean_name(name),
            testament="NEW TESTAMENT",
            position=int(value[1][:2]),
            location=value[0])
        book.save()

def create_all_books_all_chapters():
    for each_book in CHAPS:
        with open(each_book, "r+") as rh:
            chapters_dictionary = json.load(rh)

        for name, number_and_location in chapters_dictionary.items():
            if " or " in name:
                name = name.split(" or ")[0]
            book_object = Book.objects.get(name=clean_name(name))

            for number, location in number_and_location.items():
                _ = Chapter.objects.create(
                    book=book_object,
                    number=int(number),
                    location=location)

def create_all_books_all_verses():
    for each in VERSES:
        with open(each, "r+") as rh:
            verses = json.load(rh)
        for name_dash_chapter, chapter_text_dictionary in verses.items():

            parts = name_dash_chapter.split("__")
            name = parts[0]
            chapter_number = parts[1].lstrip().rstrip()

            if " or " in name:
                name = name.split(" or ")[0]
            name = clean_name(name)
            book = Book.objects.get(name=name)
            chapter = Chapter.objects.get(book=book, number=chapter_number)

            for number, text in chapter_text_dictionary.items():
                verse = Verse.objects.create(
                    chapter=chapter,
                    number=number,
                    text=text.strip())

def create_all_books_all_alt_verses():
    for each in CHAPS:
        with open(each, "r+") as rh:
            verses = json.load(rh)
        for name_dash_chapter, chapter_text_dictionary in verses.items():

            parts = name_dash_chapter.split("__")
            name = parts[0]
            chapter_number = parts[1].lstrip().rstrip()

            if " or " in name:
                name = name.split(" or ")[0]
            name = clean_name(name)
            book = Book.objects.get(name=name)

            for number, text in chapter_text_dictionary.items():
                verse = Verse(
                    book=book,
                    chapter=chapter_number,
                    number=number,
                    text=text.strip())
                verse.save()

def create_all_commentaries():
    for each in COMMENTARIES:
        with open(each, "r+") as rh:
            commentary_file = json.load(rh)

        version, _ = Version.objects.get_or_create(name="Douay-Rheims")
        commentary, _ = Commentary.objects.get_or_create(
            name="Challoner",
            version=version)

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

                commtext = CommentaryText(
                    commentary=commentary,
                    heading=heading,
                    book=book,
                    chapter=chapter,
                    verse=verse,
                    text=text)
                commtext.save()

if __name__ == "__main__":
    pass
    # create_all_books_all_chapters(CHAPS)
    # create_all_books_all_verses(VERSES)
    # create_all_commentaries(COMMENTARIES)
