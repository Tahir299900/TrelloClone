from django.contrib import admin
from .models import Project, Team, Task, UserProfile

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'created_at')
    filter_horizontal = ('members', 'projects')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'due_date', 'priority', 'status')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)
