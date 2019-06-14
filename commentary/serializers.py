from rest_framework import serializers
from .models import CommentaryText
from bible.serializers import BookSerializer

class CommentaryTextSerializer(serializers.HyperlinkedModelSerializer):
    book = BookSerializer()
    class Meta:
        model = CommentaryText
        fields = (
            'id', 'commentary_name', 'book_name', 'book', 'chapter', 'verse',  'heading', 'text', 'url'
        )
