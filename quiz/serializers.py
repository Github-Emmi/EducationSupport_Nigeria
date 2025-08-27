from rest_framework import serializers
from django.contrib.auth import get_user_model
from flashcards.models import Flashcard
from quiz.models import QuizQuestion

User = get_user_model()

class QuizQuestionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = QuizQuestion
        fields = ['id', 'user', 'topic', 'question', 'options', 
                  'correct_answer', 'created_at']
