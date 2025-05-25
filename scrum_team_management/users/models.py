from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('team_leader', 'Team Leader'),
        ('collaborator', 'Collaborator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    age = models.PositiveIntegerField(null=True, blank=True)
    # For Collaborators
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    roles_preferred = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Comma separated list of preferred roles"
    )  # Comma-separated or use ManyToMany if you want
    # Full name can be stored in first_name and last_name (from AbstractUser)
    best_competency = models.ForeignKey(
        'users.Competency',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='best_users'
    )

class Competency(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='competencies'
    )
    skill_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.skill_name