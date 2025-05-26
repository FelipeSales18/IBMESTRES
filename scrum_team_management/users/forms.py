from django import forms
from django.contrib.auth import get_user_model
from .models import Competency, User

User = get_user_model()

ROLE_CHOICES = [
    ('internal_po', 'Internal PO'),
    ('external_po', 'External PO'),
    ('developer', 'Developer'),
    ('tester', 'Tester'),
]

class CollaboratorRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    roles_preferred = forms.MultipleChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Preferred Roles"
    )
    competencies = forms.CharField(
        widget=forms.Textarea,
        help_text=("Enter your competencies one per line. "
                   "The first competency will be set as your best competency."),
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'age', 'years_of_experience']

    def clean_competencies(self):
        competencies_text = self.cleaned_data.get('competencies', '').strip()
        if not competencies_text:
            raise forms.ValidationError("Please enter at least one competency.")
        
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
                "Duplicate competencies found: " + ", ".join(duplicates)
            )
        # Optionally, you could standardize the competencies list here.
        return comp_list  # Return list for further processing

    def clean(self):
        cleaned_data = super().clean()
        # Check if passwords match.
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "Passwords do not match.")
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
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'age']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.role = 'team_leader'
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    roles_preferred = forms.MultipleChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Preferred Roles"
    )
    competencies = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter one competency per line."
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'age',
            'years_of_experience', 'best_competency', 'roles_preferred'
        ]

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