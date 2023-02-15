from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
from users.models import User
import re

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('todos')

            else:
                form.add_error(None, 'Invalid credentials')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            ''' Check the email domain '''
            allowed_domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']

            domain = email.split('@')[-1]
            if domain not in allowed_domains:
                form.add_error('email', f'Email domain {domain} is not allowed. Please use an email from one of these domains: {", ".join(allowed_domains)}')
                return render(request, 'signup.html', {'form': form})

            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            ''' Check if password is alphanumeric and 8 characters long '''
            if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[@!#$%&^*]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
                form.add_error('password', 'Password must be at least 8 characters long and contain letters, numbers, and special characters')
            
            ''' Check if passwords match '''
            if password and password2 and password != password2:
                form.add_error('password2', 'Passwords do not match')

            if form.errors:
                return render(request, 'signup.html', {'form': form})

            else:
                # Save user and redirect to login page
                user = form.save(commit=False)
                user.set_password(password)
                user.save()
                return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return render(request, 'logout.html')
