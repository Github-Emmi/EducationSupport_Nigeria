# apps/tasks/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['pending', 'in_progress', 'completed']:
            return Response({'error': 'Invalid status'}, status=400)
        
        task.status = new_status
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)
