from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm, CustomPasswordChangeForm, EditUserProfileForm
from users.models import User
from django.views import View
import re
from django.contrib import messages

class ForbiddenPageView(View):
    def get(self, request):
        return render(request, 'errors/403.html', status=403)

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

# Change Password with old password
def password_change_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomPasswordChangeForm(request.user, request.POST)

            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                new_password2 = form.cleaned_data['new_password2']

                ''' Perform password validation checks '''
                if len(new_password) < 8 or not re.search("[a-z]", new_password) or not re.search("[@!#$%&^*]", new_password) or not re.search("[A-Z]", new_password) or not re.search("[0-9]", new_password):
                    form.add_error('new_password1', 'Password must be at least 8 characters long and contain letters, numbers, and special characters')

                if new_password != new_password2:
                    form.add_error('new_password2', 'Passwords do not match')

                if form.errors:
                    return render(request, 'change_password.html', {'form': form})

                ''' If password passes all validations, save the new password '''
                fm = form.save()
                # update_session_auth_hash(fm, User)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('todos')

        else:
            form = CustomPasswordChangeForm(request.user)

        return render(request, 'change_password.html', {'form': form})
    else:
        return redirect('forbidden')

def user_details_change(request):
    if request.user.is_authenticated:
        user = request.user
        form = EditUserProfileForm(request.POST, instance=user)
        # fm = CustomPasswordChangeForm(request.user, request.POST)

        if request.method == 'POST':
            
            if form.is_valid():
                email = form.cleaned_data['email']
                # current_password = form.cleaned_data['password']
                allowed_domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']
                
                domain = email.split('@')[-1]
                if domain not in allowed_domains:
                    form.add_error('email', f'Email domain {domain} is not allowed. Please use an email from one of these domains: {", ".join(allowed_domains)}')
                
                else:
                    if form.cleaned_data.get('current_password'):
                        if user.check_password(form.cleaned_data['current_password']):
                            form.save()
                            update_session_auth_hash(request, form)
                            messages.success(request, 'Your profile has been updated.')
                            return redirect('todos')
                        else:
                            form.add_error('current_password', 'The current password is incorrect.')
                    else:
                        fm = form.save()
                        update_session_auth_hash(request, fm)
                        messages.success(request, 'Your profile has been updated.')
                        return redirect('todos')
        else:
            form = EditUserProfileForm(instance=user)

            
        return render(request, 'change_user.html', {'form': form})

    else:
        return redirect('forbidden')




