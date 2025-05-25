from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    preferred_competencies = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Enter the preferred competencies for this project, one per line.",
        required=True
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'preferred_competencies']