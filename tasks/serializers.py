from tasks.models import Task
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'priority', 
                  'status', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
