from django.db import models
from helpers.models import TimeStampedModel
from helpers.fields import AutoSlugField, AutoMultipleSlugField

from people.models import Pope

class Council(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(set_using='name')
    location = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Category(TimeStampedModel):
    """Whether a doc is constitution, declaration or decree"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Document(TimeStampedModel):
    pontiff = models.ForeignKey(Pope, on_delete=models.CASCADE)
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
        return f'{self.document.latin_name.title()} chapter {self.number}: {self.title}'

class Article(TimeStampedModel):
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
        return f'{self.chapter.document.latin_name.title()} Chapter {self.number}: {self.chapter.title}'

class Note(TimeStampedModel):
    number = models.IntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.number}. {self.article.chapter.title}'
