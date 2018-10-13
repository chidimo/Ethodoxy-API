"""models"""

from django.db import models
from universal.models import TimeStampedModel
from universal.fields import AutoSlugField, AutoMultipleSlugField

class Version(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(set_using='name')
    location = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

class Book(TimeStampedModel):
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    alt_name = models.CharField(max_length=100, blank=True)
    position = models.IntegerField()
    testament = models.CharField(max_length=20)
    slug = AutoSlugField(set_using='name')
    deutero = models.BooleanField(default=False)
    location = models.URLField(blank=True)
    about = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["position", "testament", "name"]

    def version_name(self):
        return self.version.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

    def book_chapter_count(self):
        pass
        # return self.chapter_set.count()

    def book_verse_count(self):
        pass
        # count = 0
        # for each in self.chapter_set.all():
        #     count += each.chapter_verse_count()
        # return count

    def book_word_count(self):
        pass
        # word_count = 0
        # for chapter in self.chapter_set.all():
        #     for verse in chapter.verse_set.all():
        #         word_count += len(verse.text)
        # return word_count

class Chapter(TimeStampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.IntegerField()
    location = models.URLField(blank=True)

    class Meta:
        ordering = ("book", "number")

    def book_name(self):
        return self.book.name

    def __str__(self):
        return "{} {}".format(self.book.name.title(), self.number)

    def get_absolute_url(self):
        pass

    def chapter_verse_count(self):
        pass
        # return self.verse_set.count()

class Verse(TimeStampedModel):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    number = models.IntegerField()
    text = models.CharField(max_length=600)

    class Meta:
        ordering = ["chapter", "number"]

    def book_name(self):
        return self.chapter.book.name

    def chapter_number(self):
        return self.chapter.number

    def __str__(self):
        return "{} {}: {}".format(self.chapter.book.name, self.chapter.number, self.number)

    def get_absolute_url(self):
        pass

class Commentary(TimeStampedModel):
    name = models.CharField(max_length=100)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    year = models.DateField(blank=True, null=True)

    def __str__(self):
        return "Commentary: {}".format(self.name)

class CommentaryText(TimeStampedModel):
    commentary = models.ForeignKey(Commentary, on_delete=models.CASCADE)
    heading = models.CharField(max_length=500, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter = models.IntegerField(default=1)
    slug = AutoSlugField(set_using='heading', max_length=255)
    verse = models.IntegerField(default=1)
    text = models.TextField()

    class Meta:
        ordering = ("commentary", "book", "chapter", "verse")

    def commentary_source(self):
        return "{} {} : {}".format(self.book, self.chapter, self.verse)

    def __str__(self):
        return self.heading

    def commentary_name(self):
        return self.commentary.name

    def book_name(self):
        return self.book.name

class Topic(TimeStampedModel):
    text = models.TextField()
    span = models.IntegerField()
