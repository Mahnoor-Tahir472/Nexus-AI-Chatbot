import os
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv

# 1. Load the environment variables from your .env file
load_dotenv() 

# 2. Setup and Configure the Gemini API
# This pulls the 'GEMINI_API_KEY' you saved in your .env file
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 3. Define the AI Model (using Gemini Pro)
model = genai.GenerativeModel('gemini-2.5-flash')

def home(request):
    """Serves the professional chatbot UI."""
    return render(request, 'chat/index.html')

def get_response(request):
    """
    Handles the AJAX POST request from index.html.
    Communicates with Gemini and returns the AI's response as JSON.
    """
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        
        if not user_message:
            return JsonResponse({'response': "I didn't catch that. Could you repeat it?"})
        
        try:
            # 4. Generate content using the Gemini model
            response = model.generate_content(user_message)
            
            # Use response.text to get the string output from the AI
            ai_reply = response.text
            
        except Exception as e:
            print(f"DEBUG ERROR: {e}") # This shows the error in your CMD
            ai_reply = f"Technical Error: {str(e)}" # This shows the error on your website
        return JsonResponse({'response': ai_reply})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)