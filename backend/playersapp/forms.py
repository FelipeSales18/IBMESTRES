from django import forms

from .models import Funcionario, Equipe, Projeto, Team

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

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'members']
        widgets = {
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError("O nome da equipe não pode ficar em branco.")
        # Validação de unicidade (ignora o próprio objeto em edição)
        qs = Team.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Já existe uma equipe com este nome.")
        return name

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['nome', 'descricao', 'lider', 'colaboradores']
        widgets = {
            'colaboradores': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if not nome:
            raise forms.ValidationError("O nome da equipe não pode ficar em branco.")
        qs = Equipe.objects.filter(nome__iexact=nome)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Já existe uma equipe com este nome.")
        return nome
