from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db import models
from .models import UserProfile, Task, Project

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
            messages.success(request, f'Account created successfully! Welcome {user.username}!')
            return redirect('tasks:task_list')
        else:
            # Collect all form errors into one message
            error_message = "Registration failed. Please check the following:"
            for field, errors in form.errors.items():
                error_message += f" {field.capitalize()}: {', '.join(errors)}."
            messages.error(request, error_message)
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
            messages.success(request, f'Welcome back, {username}! You have successfully logged in.')
            return redirect('tasks:task_list')
        else:
            messages.error(request, 'Login failed. Please check your username and password.')
    return render(request, 'tasks/login.html')

@require_http_methods(["GET", "POST"])
def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Goodbye, {username}! You have been logged out successfully.')
    else:
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('tasks:login')

@login_required
def task_list(request):
    tasks = Task.objects.all()
    if request.user.userprofile.role != UserProfile.Role.ADMIN:
        # For standard users, only show their created tasks or tasks assigned to them
        tasks = tasks.filter(models.Q(created_by=request.user) | models.Q(assigned_to=request.user))
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        project_id = request.POST.get('project')
        assigned_to_id = request.POST.get('assigned_to')
        
        try:
            project = Project.objects.get(id=project_id)
            assigned_to = User.objects.get(id=assigned_to_id) if assigned_to_id else None
            
            Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status,
                project=project,
                assigned_to=assigned_to,
                created_by=request.user
            )
            messages.success(request, 'Task created successfully!')
            return redirect('tasks:task_list')
        except (Project.DoesNotExist, User.DoesNotExist) as e:
            messages.error(request, 'Invalid project or user selected.')
        except Exception as e:
            messages.error(request, str(e))
    
    # Get all projects and users for the form dropdowns
    projects = Project.objects.all()
    users = User.objects.all()
    
    return render(request, 'tasks/task_create.html', {
        'projects': projects,
        'users': users
    })
# Added toast auto-dismiss timing
