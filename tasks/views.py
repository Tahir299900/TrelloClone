from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db import models
from .models import UserProfile, Task, Project, Team
from django.http import HttpResponseForbidden

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
            
            # Create or get associated UserProfile
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': user_role}
            )
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
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    project_filter = request.GET.get('project', '')
    
    tasks = Task.objects.all()
    
    # Apply filters if provided
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if project_filter:
        tasks = tasks.filter(project_id=project_filter)
        
    if request.user.userprofile.role != UserProfile.Role.ADMIN:
        # For standard users, only show their created tasks or tasks assigned to them
        tasks = tasks.filter(models.Q(created_by=request.user) | models.Q(assigned_to=request.user))
    
    # Get all available projects for the filter dropdown
    projects = Project.objects.all()
    
    context = {
        'tasks': tasks,
        'projects': projects,
        'priority_choices': Task.Priority.choices,
        'status_choices': Task.Status.choices,
        'selected_status': status_filter,
        'selected_priority': priority_filter,
        'selected_project': project_filter
    }
    
    return render(request, 'tasks/task_list.html', context)

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

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Check if user has permission to edit the task
    if request.user.userprofile.role != UserProfile.Role.ADMIN and task.created_by != request.user:
        messages.error(request, "You don't have permission to edit this task.")
        return redirect('tasks:task_list')
    
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
            
            # Update the task
            task.title = title
            task.description = description
            task.due_date = due_date
            task.priority = priority
            task.status = status
            task.project = project
            task.assigned_to = assigned_to
            task.save()
            
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks:task_list')
        except (Project.DoesNotExist, User.DoesNotExist) as e:
            messages.error(request, 'Invalid project or user selected.')
        except Exception as e:
            messages.error(request, str(e))
    
    # Get all projects and users for the form dropdowns
    projects = Project.objects.all()
    users = User.objects.all()
    
    return render(request, 'tasks/task_update.html', {
        'task': task,
        'projects': projects,
        'users': users
    })

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Check if user has permission to delete the task
    if request.user.userprofile.role != UserProfile.Role.ADMIN and task.created_by != request.user:
        messages.error(request, "You don't have permission to delete this task.")
        return redirect('tasks:task_list')
    
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted successfully!')
        return redirect('tasks:task_list')
    
    return render(request, 'tasks/task_delete.html', {'task': task})

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'ADMIN'

@login_required
def project_list(request):
    if is_admin(request.user):
        projects = Project.objects.all()
    else:
        # Get projects where the user is a team member
        projects = Project.objects.filter(teams__members=request.user).distinct()
    return render(request, 'tasks/project_list.html', {'projects': projects})

@login_required
@user_passes_test(is_admin)
def project_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        member_ids = request.POST.getlist('members')

        try:
            # Create project
            project = Project.objects.create(
                name=name,
                description=description,
                created_by=request.user
            )

            # Create team for the project
            team = Team.objects.create(
                name=f"Team {project.name}",
                leader=request.user
            )
            
            # Add selected members to the team
            team.members.add(*member_ids)
            
            # Associate team with project
            team.projects.add(project)

            messages.success(request, 'Project created successfully!')
            return redirect('tasks:project_list')
        except Exception as e:
            messages.error(request, str(e))
    
    # Get all users except the current admin
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'tasks/project_create.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    team = project.teams.first()  # Get the associated team

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        member_ids = request.POST.getlist('members')

        try:
            # Update project
            project.name = name
            project.description = description
            project.save()

            if team:
                # Update team members
                team.members.clear()
                team.members.add(*member_ids)
            else:
                # Create new team if doesn't exist
                team = Team.objects.create(
                    name=f"Team {project.name}",
                    leader=request.user
                )
                team.members.add(*member_ids)
                team.projects.add(project)

            messages.success(request, 'Project updated successfully!')
            return redirect('tasks:project_list')
        except Exception as e:
            messages.error(request, str(e))

    # Get all users except the current admin
    users = User.objects.exclude(id=request.user.id)
    selected_members = team.members.all() if team else []
    
    return render(request, 'tasks/project_update.html', {
        'project': project,
        'users': users,
        'selected_members': selected_members
    })
