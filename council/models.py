from django.db import models
from universal.models import TimeStampedModel
from universal.fields import AutoSlugField, AutoMultipleSlugField

from siteuser.models import Pontiff

class Council(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(set_using='name')
    location = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

class Category(TimeStampedModel):
    """Whether a doc is constitution, declaration or decree"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Document(TimeStampedModel):
    pontiff = models.ForeignKey(Pontiff, on_delete=models.CASCADE)
    promulgation_date = models.DateField()
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    latin_name = models.CharField(max_length=50, unique=True)
    english_name = models.CharField(max_length=150, blank=True)
    position = models.IntegerField()
    slug = AutoSlugField(set_using='latin_name')
    location = models.URLField(blank=True)

    class Meta:
        ordering = ["council", "latin_name"]

    def council_name(self):
        return self.council.name

    def __str__(self):
        return self.latin_name

class Chapter(TimeStampedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    number = models.IntegerField()

    class Meta:
        ordering = ("document", "title")

    def document_name(self):
        return self.document.name

    def __str__(self):
        return "{} {}".format(self.document.latin_name.title(), self.number)

    def get_absolute_url(self):
        pass

class Paragraph(TimeStampedModel):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    number = models.IntegerField()
    text = models.TextField()

    class Meta:
        ordering = ["chapter", "number"]

    def book_name(self):
        return self.chapter.document.name

    def chapter_number(self):
        return self.chapter.number

    def __str__(self):
        return "{} {}: {}".format(self.chapter.document.latin_name, self.chapter.number, self.number)

    def get_absolute_url(self):
        pass
