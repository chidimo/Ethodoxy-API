from rest_framework import serializers
from .models import Version, Book, Verse, Chapter

class VersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Version
        fields = ('id', 'name', 'slug', 'location', )

class BookSerializer(serializers.HyperlinkedModelSerializer):
    version = VersionSerializer()
    class Meta:
        model = Book
        fields = (
            'id', 'version', 'name', 'alt_name', 'position', 'get_absolute_url',
        'testament', 'slug', 'deutero', 'location', 'about'
        )

class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    book = BookSerializer()
    class Meta:
        model = Chapter
        fields = ('id', 'book_name', 'book', 'number', 'location', )

class VerseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Verse
        fields = ('id', 'book_name', 'chapter_number', 'number', 'text', )
