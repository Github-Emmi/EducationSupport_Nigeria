# apps/qa/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import QAHistory
from .serializers import QAHistorySerializer
from ai_integration.huggingface import HuggingFaceService

class QAView(APIView):
    def post(self, request):
        question = request.data.get('question', '')
        context = request.data.get('context', '')
        
        if not question:
            return Response({'error': 'Question is required'}, status=400)
        
        # Default context about Nigerian education if none provided
        if not context:
            context = """
            The Nigerian education system follows a 6-3-3-4 structure: 
            6 years of primary education, 3 years of junior secondary, 
            3 years of senior secondary, and 4 years of tertiary education. 
            Major challenges include inadequate funding, poor infrastructure, 
            and teacher shortages. The West African Examinations Council (WAEC) 
            and National Examinations Council (NECO) conduct major examinations.
            """
        
        hf_service = HuggingFaceService()
        result = hf_service.answer_question(context, question)
        
        # Save to history
        qa_history = QAHistory.objects.create(
            user=request.user,
            question=question,
            answer=result['answer'],
            confidence_score=result['score']
        )
        
        serializer = QAHistorySerializer(qa_history)
        return Response(serializer.data)