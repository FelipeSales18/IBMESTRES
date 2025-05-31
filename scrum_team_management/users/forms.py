from django import forms
from django.contrib.auth import get_user_model
from .models import Competency, User

User = get_user_model()

ROLE_CHOICES = [
    ('internal_po', 'PO Interno'),
    ('external_po', 'PO Externo'),
    ('developer', 'Desenvolvedor'),
    ('tester', 'Testador'),
]

class CollaboratorRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")
    roles_preferred = forms.MultipleChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Papéis Preferidos"
    )
    competencies = forms.CharField(
        widget=forms.Textarea,
        help_text=("Digite suas competências, uma por linha. "
                   "A primeira competência será definida como sua melhor competência."),
        required=True,
        label="Competências"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'age', 'years_of_experience']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'age': 'Idade',
            'years_of_experience': 'Anos de Experiência',
        }

    def clean_competencies(self):
        competencies_text = self.cleaned_data.get('competencies', '').strip()
        if not competencies_text:
            raise forms.ValidationError("Por favor, insira pelo menos uma competência.")
        
        # Process competencies: split by newline, strip and lowercase
        comp_list = [c.strip() for c in competencies_text.split('\n') if c.strip()]
        
        # Check for case-insensitive duplicate entries.
        seen = set()
        duplicates = []
        for comp in comp_list:
            comp_lower = comp.lower()
            if comp_lower in seen:
                duplicates.append(comp)
            seen.add(comp_lower)
        
        if duplicates:
            raise forms.ValidationError(
                "Competências duplicadas encontradas: " + ", ".join(duplicates)
            )
        # Optionally, you could standardize the competencies list here.
        return comp_list  # Return list for further processing

    def clean(self):
        cleaned_data = super().clean()
        # Check if passwords match.
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.role = 'collaborator'
        # Save preferred roles as comma-separated string.
        user.roles_preferred = ','.join(self.cleaned_data['roles_preferred'])
        if commit:
            user.save()
            # Process competencies: we assume clean_competencies returned a list.
            comp_list = self.cleaned_data['competencies']
            best_competency_obj = None
            for index, comp in enumerate(comp_list):
                comp_obj = Competency.objects.create(
                    user=user,
                    skill_name=comp
                )
                if index == 0:
                    best_competency_obj = comp_obj
            # Set best competency to the first competency.
            if best_competency_obj:
                user.best_competency = best_competency_obj
                user.save()
        return user

class TeamLeaderRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'age']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'age': 'Idade',
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', "As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.role = 'team_leader'
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ExternalPORegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'age']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'age': 'Idade',
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', "As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.role = 'external_po'
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    roles_preferred = forms.MultipleChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Papéis Preferidos"
    )
    competencies = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Digite uma competência por linha.",
        label="Competências"
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'age',
            'years_of_experience', 'best_competency', 'roles_preferred'
        ]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'age': 'Idade',
            'years_of_experience': 'Anos de Experiência',
            'best_competency': 'Melhor Competência',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate roles_preferred as a list
        if self.instance.pk and self.instance.roles_preferred:
            self.fields['roles_preferred'].initial = [
                r.strip() for r in self.instance.roles_preferred.split(',')
            ]
        # Prepopulate competencies field with user's current competencies (except best)
        if self.instance.pk:
            comps = self.instance.competencies.exclude(pk=self.instance.best_competency_id)
            self.fields['competencies'].initial = '\n'.join([c.skill_name for c in comps])

    def save(self, commit=True):
        user = super().save(commit=False)
        # Save preferred roles as comma-separated string
        roles = self.cleaned_data.get('roles_preferred', [])
        user.roles_preferred = ','.join(roles)
        if commit:
            user.save()
            # Update competencies
            comps_str = self.cleaned_data.get('competencies', '')
            comps = [c.strip() for c in comps_str.split('\n') if c.strip()]
            # Remove old (non-best) competencies
            user.competencies.exclude(pk=user.best_competency_id).delete()
            # Add new competencies
            for c in comps:
                if not user.competencies.filter(skill_name__iexact=c).exists():
                    Competency.objects.create(user=user, skill_name=c)
        return user