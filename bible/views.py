from collections import OrderedDict

from django.http import JsonResponse, HttpResponse

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Version, Book, Chapter, Verse
from .serializers import VersionSerializer, BookSerializer, ChapterSerializer, VerseSerializer


class VersionViewSet(viewsets.ModelViewSet):

    def create(self, request):
        print(request)
        if request.method == 'POST':
            data = request.data
            name = data['name']

            try:
                Version.objects.get(name=name)
                return JsonResponse(f'{name} version already exists.', status=400, safe=False)
            except:
                version, created = Version.objects.get_or_create(name=name)
                return JsonResponse(f'{name} version created.', status=201, safe=False)      

    queryset = Version.objects.all()
    serializer_class = VersionSerializer

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            verses = Verse.objects.filter(chapter__book=book)

            page = self.paginate_queryset(verses)
            if page is not None:
                data = []
                for verse in page:
                    serialized_verse = VerseSerializer(verse)
                    data.append(serialized_verse.data)
                return self.get_paginated_response(data)
        except Book.DoesNotExist:
            return Response({'message' : f'Book with id {pk} does not exist'})


class ChaptersViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class VersesViewSet(viewsets.ModelViewSet):
    queryset = Verse.objects.all()
    serializer_class = VerseSerializer

@api_view(['GET'])
def get_chapter(request, book_pk, pk):
    """Return chapter of particular book"""

    return_data = OrderedDict()
    chapter = Chapter.objects.get(pk=pk)

    for verse in chapter.verse_set.all():
        return_data[verse.number] = verse.text
    return JsonResponse(return_data)

@api_view(['GET'])
def get_book(request, pk):
    """Return single book with associated chapters and verses"""
    book = Book.objects.get(pk=pk)
    verses = Verse.objects.filter(chapter__book=book)
    data = []
    for verse in verses:
        serialized_verse = VerseSerializer(verse)
        data.append(serialized_verse.data)
        print(serialized_verse)
    return JsonResponse(data, safe=False)
