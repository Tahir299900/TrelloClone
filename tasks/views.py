from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import UserProfile

def index(request):
    return render(request, 'tasks/index.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('tasks:task_list')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Determine if this is the first user (make them admin)
            if User.objects.count() == 1:
                user_role = UserProfile.Role.ADMIN
                user.is_staff = True  # Give admin access to Django admin
                user.is_superuser = True  # Give full permissions
                user.save()
            else:
                user_role = UserProfile.Role.STANDARD
            
            # Create associated UserProfile
            UserProfile.objects.create(user=user, role=user_role)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('tasks:task_list')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return render(request, 'tasks/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('tasks:task_list')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Ensure UserProfile exists
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': UserProfile.Role.STANDARD}
            )
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('tasks:task_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'tasks/login.html')

@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('tasks:login')

@login_required
def task_list(request):
    tasks = []
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        # We'll implement this later when we have our models
        pass
    return render(request, 'tasks/task_create.html')
