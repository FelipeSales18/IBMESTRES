from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from playersapp.models import Funcionario

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('leader', 'Líder'),
        ('collaborator', 'Colaborador'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Tipo de Usuário", required=True)
    full_name = forms.CharField(max_length=150, label="Nome Completo", required=True)
    empresa = forms.CharField(max_length=150, label="Empresa", required=False)
    anos_como_lider = forms.IntegerField(label="Anos como Líder", required=False)

    # Campos adicionais para colaboradores
    idade = forms.IntegerField(required=False, label="Idade")
    hard_skils = forms.CharField(max_length=300, required=False, label="Hard Skills")
    soft_skils = forms.CharField(max_length=300, required=False, label="Soft Skills")
    ex_developer = forms.BooleanField(required=False, label="Experiência como Developer")
    ex_product_owner = forms.BooleanField(required=False, label="Experiência como Product Owner")
    ex_scrum_master = forms.BooleanField(required=False, label="Experiência como Scrum Master")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'full_name']

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role == 'leader':
            if not cleaned_data.get('empresa') or not cleaned_data.get('anos_como_lider'):
                raise forms.ValidationError("Os campos 'Empresa' e 'Anos como Líder' são obrigatórios para Líderes.")
        elif role == 'collaborator':
            if not cleaned_data.get('idade') or not cleaned_data.get('hard_skils') or not cleaned_data.get('soft_skils'):
                raise forms.ValidationError("Todos os campos de colaborador são obrigatórios.")
        return cleaned_data