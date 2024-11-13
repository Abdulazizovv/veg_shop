from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import login


def index(request):
    return render(request, 'index.html')


def register_user(request):

    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('index')

    if request.method == 'POST':
        first_name = request.POST['firstName']
        email = request.POST['emailAddress']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        if password == confirm_password:
            try:
                user = CustomUser.objects.create_user(email=email, first_name=first_name, password=password)
                user.save()
                messages.success(request, 'User registered successfully')
                return redirect('index')
            except:
                messages.error(request, 'User with this email already exists')
                return render(request, 'register.html')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST['emailAddress']
        password = request.POST['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            messages.error(request, 'User not found')
            return render(request, 'login.html')
        else:
            if user.check_password(password):
                messages.success(request, 'Login successful')
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid password')
                return render(request, 'login.html')

    return render(request, 'login.html')