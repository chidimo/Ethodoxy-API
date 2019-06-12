from rest_framework import generics
from ..models import CommentaryText
from . import serializers

class CommentaryTextListView(generics.ListAPIView):
    queryset = CommentaryText.objects.all()
    serializer_class = serializers.CommentaryTextSerializer
