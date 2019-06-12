"""REST api"""

from rest_framework import serializers
from ..models import CommentaryText

class CommentaryTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentaryText
        fields = (
            "commentary_name", "book_name", "book",
            "chapter", "verse",  "heading", "text")
