"""models"""

from django.db import models
from django.shortcuts import reverse

from helpers.models import TimeStampedModel
from helpers.fields import AutoSlugField, AutoMultipleSlugField

class Version(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(set_using='name')

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

class Book(TimeStampedModel):
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    alt_name = models.CharField(max_length=100, blank=True)
    position = models.IntegerField()
    testament = models.CharField(max_length=20)
    slug = AutoSlugField(set_using='name')
    deutero = models.BooleanField(default=False)
    about = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["position", "testament", "name"]

    def version_name(self):
        return self.version.name

    def __str__(self):
        return self.name

class Chapter(TimeStampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.IntegerField()

    class Meta:
        ordering = ("book", "number")

    def book_name(self):
        return self.book.name

    def __str__(self):
        return f'{self.book.name.title()} {self.number}'

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
        return f'{self.chapter.book.name.title()} {self.chapter.number}: {self.number}'
