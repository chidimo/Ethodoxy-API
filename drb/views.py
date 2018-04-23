from django.shortcuts import render
from django.views import generic
from pure_pagination.mixins import PaginationMixin
from .models import Version, Book, Chapter, Verse, Commentary, CommentaryText

class Index(PaginationMixin, generic.ListView):
    model = Book
    template_name = "drb/index.html"
    context_object_name = "books"
    paginate_by = 25

class BookDetail(generic.DetailView):
    model = Book
    context_object_name = "book"
    template_name = "drb/book.html"

class ChapterDetail(generic.DetailView):
    model = Chapter
    context_object_name = "chapter"
    template_name = "drb/chapter.html"

class VerseDetail(generic.DetailView):
    model = Verse
    context_object_name = "verse"
    template_name = "drb/verse.html"

class CommentaryByChapter(PaginationMixin, generic.ListView):
    model = CommentaryText
    template_name = "drb/commentary_index.html"
    context_object_name = "commentaries"
    paginate_by = 25

class CommentaryTextDetail(generic.DetailView):
    model = CommentaryText
    template_name = "drb/commentary_detail.html"
    context_object_name = "commentary"
