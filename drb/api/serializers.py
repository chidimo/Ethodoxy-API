"""REST api"""

from rest_framework import serializers
from ..models import Book, Verse, Chapter, CommentaryText

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ("book_name", "chapter_number", "number", "text", )
       
class VerseSerializerHyperlinked(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Verse
        fields = ("book_name", "chapter_number", "number", "text", )

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ("book_name", "book", "chapter_number", "location", )

class CommentaryTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentaryText
        fields = (
            "commentary_name", "book_name", "book",
            "chapter", "verse",  "heading", "text")
