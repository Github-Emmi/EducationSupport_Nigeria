from rest_framework import serializers
from stories.models import Story

class StorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Story
        fields = ['id', 'user', 'title', 'content', 'sentiment_score', 
                  'sentiment_label', 'created_at']
        read_only_fields = ['sentiment_score', 'sentiment_label']
