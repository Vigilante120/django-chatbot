from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth 
from django.contrib.auth.models import User

from django.utils import timezone
from .models import Chat

# Create your views here.


openai_api_key = ''
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message},
    ],
   
)


    for chunk in response:
        
        answer = response['choices'][0]['message']['content']
    return answer 

def bot(request):
    chats = Chat.objects.filter(user=request.user.id)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'response': response, 'message': message})
    return render(request, 'chatbot.html', {'chats':chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('bot')
        else:
            error_message = 'username or password not correct'
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
                error_message = 'Error occured while creating user'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'password does not match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')