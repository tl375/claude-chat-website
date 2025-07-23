from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from openai import OpenAI

# Load environment variables from .env file
try:
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
    pass

def homepage(request):
    return render(request, 'main/homepage.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Get OpenAI API key from environment variable
            api_key = os.getenv('OPENAI_API_KEY')
            
            if not api_key:
                return JsonResponse({
                    'response': 'OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.',
                    'status': 'error'
                })
            
            # Initialize OpenAI client
            client = OpenAI(api_key=api_key)
            
            # Make API call to OpenAI GPT
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                max_tokens=500,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            
            response_message = response.choices[0].message.content.strip()
            
            return JsonResponse({
                'response': response_message,
                'status': 'success'
            })
            
        except Exception as e:
            # Log the actual error for debugging
            print(f"OpenAI API Error: {str(e)}")
            
            # Check specific error types
            if "invalid_api_key" in str(e).lower() or "authentication" in str(e).lower():
                return JsonResponse({
                    'response': 'API key is invalid. Please check your OpenAI API key configuration.',
                    'status': 'error'
                })
            elif "rate_limit" in str(e).lower() or "quota" in str(e).lower():
                return JsonResponse({
                    'response': 'OpenAI API quota exceeded or rate limit hit. Please check your usage at https://platform.openai.com/',
                    'status': 'error'
                })
            else:
                # Generic fallback responses
                fallback_responses = [
                    "I'm currently experiencing some technical difficulties. Please try again later.",
                    "Sorry, I couldn't process your request right now. Please check back soon.",
                    "I'm having trouble connecting to my language model. Please try again.",
                    "Technical issues are preventing me from responding properly. Please retry your message.",
                    "I'm temporarily unavailable. Please try your question again in a moment."
                ]
                
                import random
                response_message = random.choice(fallback_responses)
                
                return JsonResponse({
                    'response': response_message,
                    'status': 'fallback'
                })
    
    return JsonResponse({'error': 'Invalid request method'})
