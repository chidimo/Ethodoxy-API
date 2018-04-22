from rest_framework import generics
from ..models import Book, Chapter, Verse, CommentaryText
from . import serializers

class VerseListView(generics.ListAPIView):
    queryset = Verse.objects.all()
    serializer_class = serializers.VerseSerializer

class VerseDetailView(generics.RetrieveAPIView):
    queryset = Verse.objects.all()
    serializer_class = serializers.VerseSerializer

class ChapterListView(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = serializers.ChapterSerializer

class CommentaryTextListView(generics.ListAPIView):
    queryset = CommentaryText.objects.all()
    serializer_class = serializers.CommentaryTextSerializer
