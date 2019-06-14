from rest_framework import generics

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import CommentaryTextSerializer
from .models import CommentaryText

class CommentaryTextViewSet(viewsets.ModelViewSet):
    queryset = CommentaryText.objects.all()
    serializer_class = CommentaryTextSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Unable to delete'})
    
    def create(self, request):
        return Response({'message': 'Unable to create'})

    def update(self, request, pk=None):
        return Response({'message': 'Unable to update'})

    def partial_update(self, request, pk=None):
        return Response({'message': 'Unable to partial update'})
