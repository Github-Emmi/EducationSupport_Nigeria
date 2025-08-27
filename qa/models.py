from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# qa/models.py
class QAHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qa_history')
    question = models.TextField()
    answer = models.TextField()
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Q&A History'
        verbose_name_plural = 'Q&A History'