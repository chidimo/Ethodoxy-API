from collections import OrderedDict

from django.http import JsonResponse, HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Version, Book, Chapter, Verse
from .serializers import VersionSerializer, BookSerializer, ChapterSerializer, VerseSerializer


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

    def create(self, request):
        if request.method == 'POST':
            data = request.data
            name = data['name']

            try:
                Version.objects.get(name=name)
                return JsonResponse(f'{name} version already exists.', status=400, safe=False)
            except:
                version, created = Version.objects.get_or_create(name=name)
                return JsonResponse(f'{name} version created.', status=201, safe=False)


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

    def retrieve(self, request, pk=None):
        try:
            verses = Verse.objects.filter(chapter__book__pk=pk)

            page = self.paginate_queryset(verses)
            if page is not None:
                data = []
                for verse in page:
                    serialized_verse = VerseSerializer(verse, context={'request': request})
                    data.append(serialized_verse.data)
                return self.get_paginated_response(data)
        except Book.DoesNotExist:
            return Response({'message' : f'Book with id {pk} does not exist'})

    def create(self, request):
        return Response({'message': 'Unable to create'})

    def update(self, request, pk=None):
        return Response({'message': 'Unable to update'})

    def partial_update(self, request, pk=None):
        return Response({'message': 'Unable to partial update'})


class ChaptersViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

    def retrieve(self, request, pk=None):
        try:
            verses = Verse.objects.filter(chapter__book__pk=pk)
            page = self.paginate_queryset(verses)
            if page is not None:
                data = []
                for verse in page:
                    serialized_verse = VerseSerializer(verse, context={'request': request})
                    data.append(serialized_verse.data)
                return self.get_paginated_response(data)

        except Chapter.DoesNotExist:
            return Response({'message' : f'Chapter with id {pk} does not exist'})

        return Response({'message': 'Unable to retrieve'})

    def create(self, request):
        return Response({'message': 'Unable to create'})

    def update(self, request, pk=None):
        return Response({'message': 'Unable to update'})

    def partial_update(self, request, pk=None):
        return Response({'message': 'Unable to partial update'})

class VersesViewSet(viewsets.ModelViewSet):
    queryset = Verse.objects.all()
    serializer_class = VerseSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})

    def create(self, request):
        return Response({'message': 'Unable to create'})

    def update(self, request, pk=None):
        return Response({'message': 'Unable to update'})

    def partial_update(self, request, pk=None):
        return Response({'message': 'Unable to partial update'})
