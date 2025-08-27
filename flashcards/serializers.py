from rest_framework import serializers
from django.contrib.auth import get_user_model
from flashcards.models import Flashcard

User = get_user_model()


class FlashcardSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Flashcard
        fields = ['id', 'user', 'question', 'answer', 'category', 
                  'difficulty', 'review_count', 'last_reviewed', 'created_at']
        read_only_fields = ['review_count', 'last_reviewed']