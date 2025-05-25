from django import forms
from .models import Team
from users.models import User

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']


class ManualTeamForm(forms.Form):
    name = forms.CharField(label="Nome da equipe", max_length=100, required=True)
    num_members = forms.ChoiceField(
        label="Quantidade de colaboradores",
        choices=[(str(i), str(i)) for i in range(3, 11)],
        required=True
    )
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='collaborator'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Colaboradores"
    )