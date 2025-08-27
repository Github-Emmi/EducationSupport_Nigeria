# stories/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Story
from .serializers import StorySerializer
from ai_integration.huggingface import HuggingFaceService

class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    
    def get_queryset(self):
        return Story.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def analyze_sentiment(self, request, pk=None):
        story = self.get_object()
        hf_service = HuggingFaceService()
        
        # Analyze sentiment
        sentiment_result = hf_service.analyze_sentiment(story.content)
        
        # Update story with sentiment
        story.sentiment_score = sentiment_result['score']
        story.sentiment_label = sentiment_result['label']
        story.save()
        
        serializer = self.get_serializer(story)
        return Response(serializer.data)