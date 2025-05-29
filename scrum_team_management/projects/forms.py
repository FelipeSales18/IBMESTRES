from django import forms
from .models import Project, ProjectUpdate
from users.models import User

class ProjectForm(forms.ModelForm):
    preferred_competencies = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Enter the preferred competencies for this project, one per line.",
        required=True
    )
    testers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='collaborator'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'preferred_competencies', 'testers']

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectUpdate
        fields = ['what_was_done', 'how_project_is_going', 'setbacks']
        widgets = {
            'what_was_done': forms.Textarea(attrs={'rows': 3}),
            'how_project_is_going': forms.Textarea(attrs={'rows': 3}),
            'setbacks': forms.Textarea(attrs={'rows': 2}),
        }

class ManualTeamForm(forms.Form):
    name = forms.CharField(label="Team Name")
    num_members = forms.IntegerField(label="Number of Members")
    members = forms.ModelMultipleChoiceField(queryset=User.objects.filter(role='collaborator'))
    internal_po = forms.ModelChoiceField(queryset=User.objects.filter(role='collaborator'))
    external_po = forms.ModelChoiceField(
        queryset=User.objects.filter(role='external_po'),
        required=False,  # <-- Make it optional
        label="External PO (optional)"
    )