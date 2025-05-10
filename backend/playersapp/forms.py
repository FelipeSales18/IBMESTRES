from django import forms

from .models import Funcionario, Equipe

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = [
            'nome',
            'idade',
            'hard_skils',
            'soft_skils',
            'ex_developer',
            'ex_product_owner',
            'ex_scrum_master',
        ]

class AssociarEquipeForm(forms.Form):
    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.all(),
        label="Colaborador",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    equipe = forms.ModelChoiceField(
        queryset=Equipe.objects.all(),  # Certifique-se de que as equipes estão sendo carregadas
        label="Equipe",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
