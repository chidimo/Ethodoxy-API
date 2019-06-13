from rest_framework import generics

from rest_framework import viewsets
# from rest_framework.decorators import api_view

from .serializers import CommentaryTextSerializer
from .models import CommentaryText

class CommentaryTextViewSet(viewsets.ModelViewSet):
    queryset = CommentaryText.objects.all()
    serializer_class = CommentaryTextSerializer
