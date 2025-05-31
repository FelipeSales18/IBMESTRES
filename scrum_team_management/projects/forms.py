from django import forms
from .models import Project, ProjectUpdate
from users.models import User

class ProjectForm(forms.ModelForm):
    preferred_competencies = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Digite as competências preferidas para este projeto, uma por linha.",
        required=True,
        label="Competências Preferidas"
    )
    testers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='collaborator'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Testadores"
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'preferred_competencies', 'testers']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
        }

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectUpdate
        fields = ['what_was_done', 'how_project_is_going', 'setbacks']
        widgets = {
            'what_was_done': forms.Textarea(attrs={'rows': 3}),
            'how_project_is_going': forms.Textarea(attrs={'rows': 3}),
            'setbacks': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'what_was_done': 'O que foi feito',
            'how_project_is_going': 'Como o projeto está indo',
            'setbacks': 'Dificuldades',
        }

class ManualTeamForm(forms.Form):
    name = forms.CharField(label="Nome da Equipe")
    num_members = forms.IntegerField(label="Quantidade de Membros")
    members = forms.ModelMultipleChoiceField(queryset=User.objects.filter(role='collaborator'), label="Colaboradores")
    internal_po = forms.ModelChoiceField(queryset=User.objects.filter(role='collaborator'), label="PO Interno")
    external_po = forms.ModelChoiceField(
        queryset=User.objects.filter(role='external_po'),
        required=False,
        label="PO Externo (opcional)"
    )