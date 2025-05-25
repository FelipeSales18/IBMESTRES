from django import forms
from django.contrib.auth import get_user_model
from .models import Competency

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