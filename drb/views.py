from django.shortcuts import render
from django.views import generic
from pure_pagination.mixins import PaginationMixin
from .models import Version, Book, Chapter, Verse, Commentary, CommentaryText

class Index(PaginationMixin, generic.ListView):
    model = Book
    template_name = "drb/index.html"
    context_object_name = "book_list"

class BookChapters(generic.ListView):
    model = Book
    context_object_name = "book_chapter_list"
    template_name = "drb/book_chapter_list.html"

    def book(self):
        return Book.objects.get(pk=self.kwargs['pk'], slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book()
        return context

    def get_queryset(self):
        return self.book().chapter_set.all()

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
    paginate_by = 20

class CommentaryTextDetail(generic.DetailView):
    model = CommentaryText
    template_name = "drb/commentary_detail.html"
    context_object_name = "commentary"
