from rest_framework import serializers
from django.contrib.auth import get_user_model
from qa.models import QAHistory

class QAHistorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = QAHistory
        fields = ['id', 'user', 'question', 'answer', 
                  'confidence_score', 'created_at']
