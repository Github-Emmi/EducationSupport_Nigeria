# ai_integration/huggingface.py
import requests
from django.conf import settings
from transformers import pipeline
import json

class HuggingFaceService:
    def __init__(self):
        self.api_key = settings.HUGGING_FACE_API_KEY
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
    def analyze_sentiment(self, text):
        """Analyze sentiment of text using Hugging Face API"""
        API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
        
        payload = {"inputs": text}
        response = requests.post(API_URL, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            results = response.json()[0]
            # Get highest scoring sentiment
            best_result = max(results, key=lambda x: x['score'])
            return {
                'label': best_result['label'],
                'score': best_result['score']
            }
        return {'label': 'neutral', 'score': 0.0}
    
    def generate_quiz_questions(self, topic, num_questions=5):
        """Generate quiz questions using Hugging Face API"""
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
        
        prompt = f"Generate {num_questions} multiple choice questions about {topic} for Nigerian students. Format: Q: [question] A) [option] B) [option] C) [option] D) [option] Answer: [correct option]"
        
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            generated_text = response.json()[0]['generated_text']
            # Parse the generated questions
            questions = self._parse_quiz_questions(generated_text)
            return questions
        return []
    
    def answer_question(self, context, question):
        """Answer questions using Hugging Face QA model"""
        API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
        
        payload = {
            "inputs": {
                "question": question,
                "context": context
            }
        }
        response = requests.post(API_URL, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return {
                'answer': result.get('answer', 'I could not find an answer'),
                'score': result.get('score', 0.0)
            }
        return {'answer': 'Unable to process question', 'score': 0.0}
    
    def _parse_quiz_questions(self, text):
        """Parse generated quiz questions into structured format"""
        questions = []
        lines = text.split('\n')
        
        current_question = {}
        for line in lines:
            if line.startswith('Q:'):
                if current_question:
                    questions.append(current_question)
                current_question = {
                    'question': line[2:].strip(),
                    'options': []
                }
            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                if current_question:
                    current_question['options'].append(line.strip())
            elif line.startswith('Answer:'):
                if current_question:
                    current_question['correct_answer'] = line[7:].strip()
        
        if current_question:
            questions.append(current_question)
        
        return questions