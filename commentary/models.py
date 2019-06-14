from django.db import models
from helpers.models import TimeStampedModel
from helpers.fields import AutoSlugField, AutoMultipleSlugField

from bible.models import Version, Book

class Commentary(TimeStampedModel):
    name = models.CharField(max_length=100)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    year = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Commentary: {self.name}'

class CommentaryText(TimeStampedModel):
    commentary = models.ForeignKey(Commentary, on_delete=models.CASCADE)
    heading = models.CharField(max_length=500, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter = models.IntegerField(default=1)
    slug = AutoSlugField(set_using='heading', max_length=255)
    verse = models.IntegerField(default=1)
    text = models.TextField()

    class Meta:
        ordering = ('commentary', 'book', 'chapter', 'verse')

    def commentary_source(self):
        return f'{self.book} {self.chapter} : {self.verse}'

    def __str__(self):
        return self.heading

    def commentary_name(self):
        return self.commentary.name

    def book_name(self):
        return self.book.name

class Topic(TimeStampedModel):
    text = models.TextField()
    span = models.IntegerField()
