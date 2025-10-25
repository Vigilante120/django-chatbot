from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
import os

from django.utils import timezone
from django.conf import settings

gemini_api_key = settings.GEMINI_API_KEY
genai.configure(api_key=gemini_api_key)

def ask_openai(message):
    try:
        # Use the latest available Gemini Flash model
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(message)
        answer = response.text.strip()
        return answer
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Sorry, I couldn't get a reply from the AI right now."

# Create your views here.
def bot(request):
    chats = Chat.objects.filter(user=request.user.id)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('bot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('bot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
