from collections import OrderedDict

from django.core import serializers

from django.shortcuts import render
from django.views import generic
from pure_pagination.mixins import PaginationMixin
from .models import Version, Book, Chapter, Verse, Commentary, CommentaryText
from django.http import JsonResponse, HttpResponse

def douay_rheims_bible(request):
    template = 'drb/douay_rheims_bible.html'
    context = {}
    context['books'] = Book.objects.all()
    return render(request, template, context)

def get_chapter(request, pk):
    return_data = OrderedDict()
    chapter = Chapter.objects.get(pk=pk)
    for verse in chapter.verse_set.all():
        return_data[verse.number] = verse.text
    return JsonResponse(return_data)

class CommentaryByChapter(PaginationMixin, generic.ListView):
    model = CommentaryText
    template_name = "drb/challoner.html"
    context_object_name = "commentaries"
    paginate_by = 20
