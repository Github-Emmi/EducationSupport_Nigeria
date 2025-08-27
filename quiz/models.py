from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# quiz/models.py
class QuizQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_questions')
    topic = models.CharField(max_length=100)
    question = models.TextField()
    options = models.JSONField()  # Store as JSON array
    correct_answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']