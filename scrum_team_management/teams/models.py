from django.db import models
from django.conf import settings
from projects.models import Project
from django.contrib.auth import get_user_model
User = get_user_model()

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='teams', null=True, blank=True)
    max_size = models.PositiveIntegerField(default=9)
    #team_creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_teams')

    def __str__(self):
        return self.name

class TeamAssignment(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('Team Leader', 'Team Leader'), ('Collaborator', 'Collaborator')])
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.team.name}"