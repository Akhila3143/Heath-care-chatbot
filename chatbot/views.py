from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from .forms import UserRegisterForm
from .models import ChatLog
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import os
import json

# Function to load symptoms and tips from JSON file
def load_symptoms_tips():
    with open(os.path.join(os.path.dirname(__file__), 'symptoms_tips.json'), 'r') as file:
        return json.load(file)['symptoms_tips']

# Load symptoms and tips once and cache them
symptoms_tips = load_symptoms_tips()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'chatbot/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('chatbot-interface')
    else:
        form = AuthenticationForm()
    return render(request, 'chatbot/login.html', {'form': form})

def home(request):
    login_success = request.GET.get('login_success', False)
    context = {'login_success': login_success}
    return render(request, 'chatbot/home.html', context)

def services(request):
    return render(request, 'chatbot/services.html')

def about_us(request):
    return render(request, 'chatbot/about_us.html')

def faq(request):
    return render(request, 'chatbot/faq.html')

@login_required
def chatbot_interface(request):
    username = request.user.username
    return render(request, 'chatbot/chatbot_interface.html', {'username': username})

@login_required
def get_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        symptoms = extract_symptoms(user_message)  # Function to extract symptoms from the user message
        responses = []

        for symptom in symptoms:
            response_data = generate_response(symptom)
            chat_log = ChatLog(user=request.user, message=symptom, response=response_data['tip'])
            chat_log.save()
            responses.append(response_data)

        return JsonResponse({'responses': responses})

    return JsonResponse({'error': 'Invalid request method'})

def extract_symptoms(user_message):
    # Implement your logic to extract symptoms from the user input
    # You can use spaCy or regular expressions to identify symptoms
    # For simplicity, assume splitting by comma for multiple symptoms
    return user_message.split(',')

def generate_response(symptom):
    global symptoms_tips
    for item in symptoms_tips:
        if item['symptom'].lower() in symptom.lower():
            return {
                'tip': item['tip'],
                'food': item['food'],
                'medicine': item['medicine']
            }
    return {
        'tip': "I'm sorry, I didn't understand that. Can you please rephrase?",
        'food': '',
        'medicine': ''
    }
