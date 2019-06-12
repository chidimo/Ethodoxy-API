from collections import OrderedDict

from django.core import serializers

from django.shortcuts import render
from django.views import generic
from pure_pagination.mixins import PaginationMixin
from .models import Version, Book, Chapter, Verse
from django.http import JsonResponse, HttpResponse

def bible_index(request):
    template = 'bible/index.html'
    context = {}
    context['books'] = Book.objects.all()
    return render(request, template, context)

def get_chapter(request, pk):
    return_data = OrderedDict()
    chapter = Chapter.objects.get(pk=pk)
    for verse in chapter.verse_set.all():
        return_data[verse.number] = verse.text
    return JsonResponse(return_data)
