from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Flashcard
from .serializers import FlashcardSerializer

class FlashcardViewSet(viewsets.ModelViewSet):
    serializer_class = FlashcardSerializer
    
    def get_queryset(self):
        return Flashcard.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        flashcard = self.get_object()
        flashcard.review_count += 1
        flashcard.last_reviewed = timezone.now()
        flashcard.save()
        
        serializer = self.get_serializer(flashcard)
        return Response(serializer.data)