# apps/quiz/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import QuizQuestion
from .serializers import QuizQuestionSerializer
from ai_integration.huggingface import HuggingFaceService

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizQuestionSerializer
    
    def get_queryset(self):
        return QuizQuestion.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        topic = request.data.get('topic', '')
        num_questions = request.data.get('num_questions', 5)
        
        if not topic:
            return Response({'error': 'Topic is required'}, status=400)
        
        hf_service = HuggingFaceService()
        questions = hf_service.generate_quiz_questions(topic, num_questions)
        
        # Save generated questions
        created_questions = []
        for q in questions:
            quiz_question = QuizQuestion.objects.create(
                user=request.user,
                topic=topic,
                question=q['question'],
                options=q['options'],
                correct_answer=q['correct_answer']
            )
            created_questions.append(quiz_question)
        
        serializer = self.get_serializer(created_questions, many=True)
        return Response(serializer.data)
