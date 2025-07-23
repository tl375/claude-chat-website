from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from anthropic import Anthropic

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
            
            # Get Claude API key from environment variable
            api_key = os.getenv('ANTHROPIC_API_KEY')
            
            if not api_key:
                return JsonResponse({
                    'response': 'Claude API key not configured. Please set ANTHROPIC_API_KEY environment variable.',
                    'status': 'error'
                })
            
            # Initialize Claude client
            client = Anthropic(api_key=api_key)
            
            # Make API call to Claude
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[
                    {
                        "role": "user", 
                        "content": f"You are a helpful AI assistant. Provide clear, concise, and helpful responses.\n\nUser: {user_message}"
                    }
                ]
            )
            
            response_message = response.content[0].text.strip()
            
            return JsonResponse({
                'response': response_message,
                'status': 'success'
            })
            
        except Exception as e:
            # Log the actual error for debugging
            print(f"Claude API Error: {str(e)}")
            
            # Check specific error types
            if "invalid_api_key" in str(e).lower():
                return JsonResponse({
                    'response': 'API key is invalid. Please check your Claude API key configuration.',
                    'status': 'error'
                })
            elif "insufficient_quota" in str(e).lower() or "exceeded your current quota" in str(e).lower():
                return JsonResponse({
                    'response': 'Claude API quota exceeded. Please add credits to your Anthropic account at https://console.anthropic.com/',
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
