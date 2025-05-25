from django.contrib import admin
from .models import Team, TeamAssignment

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(TeamAssignment)
class TeamAssignmentAdmin(admin.ModelAdmin):
    list_display = ('team', 'user', 'role', 'assigned_at')
    list_filter = ('team', 'role')
    search_fields = ('user__username',)