from django import forms
from .models import Funcionario

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
