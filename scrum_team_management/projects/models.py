from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    team_leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects_lead')
    preferred_competencies = models.TextField(blank=True, help_text="Enter the preferred competencies for this project, one per line.")
    testers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects_as_tester',
        blank=True,
        limit_choices_to={'role': 'collaborator'}
    )

    def __str__(self):
        return self.name

class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    what_was_done = models.TextField()
    how_project_is_going = models.TextField()
    setbacks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Update for {self.project.name} on {self.created_at}'