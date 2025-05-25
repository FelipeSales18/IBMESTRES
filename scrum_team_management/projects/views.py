from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project
from .forms import ProjectForm
from teams.forms import ManualTeamForm
from teams.models import Team, TeamAssignment
from users.models import User
from django.http import HttpResponse
import random
from datetime import datetime
from django.utils import timezone

# Funções utilitárias para seleção balanceada
def get_collaborators_by_skill(collaborators, skill):
    return [c for c in collaborators if skill.lower() in (c.roles_preferred or '').lower()]

def generate_balanced_team(collaborators, min_size=3, max_size=10):
    skills = ['frontend', 'backend', 'qa', 'devops', 'ux']
    selected = []
    used_ids = set()
    # Garante pelo menos 1 de cada skill principal, se possível
    for skill in skills:
        skill_collabs = [c for c in collaborators if c.id not in used_ids and skill in (c.roles_preferred or '').lower()]
        if skill_collabs:
            chosen = random.choice(skill_collabs)
            selected.append(chosen)
            used_ids.add(chosen.id)
    # Preenche até o máximo, tentando equilibrar
    remaining = [c for c in collaborators if c.id not in used_ids]
    while len(selected) < min_size and remaining:
        chosen = random.choice(remaining)
        selected.append(chosen)
        used_ids.add(chosen.id)
        remaining = [c for c in collaborators if c.id not in used_ids]
    while len(selected) < max_size and remaining:
        chosen = random.choice(remaining)
        selected.append(chosen)
        used_ids.add(chosen.id)
        remaining = [c for c in collaborators if c.id not in used_ids]
    return selected[:max_size]

class TeamLeaderRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Adjust this logic if necessary for your custom user model
        return self.request.user.role == 'team_leader'

class ProjectCreateView(LoginRequiredMixin, TeamLeaderRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create_project.html'

    def form_valid(self, form):
        form.instance.team_leader = self.request.user
        self.object = form.save()  # Save the object and set self.object
        return redirect(reverse('project_confirmation', kwargs={'project_id': self.object.id}))
    
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

class ProjectUpdateView(LoginRequiredMixin, TeamLeaderRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/edit_project.html'
    success_url = reverse_lazy('project_list')

class ProjectDeleteView(LoginRequiredMixin, TeamLeaderRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

class ProjectConfirmationView(LoginRequiredMixin, TeamLeaderRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_confirmation.html'
    context_object_name = 'project'
    
    # Use a different URL parameter name (project_id) instead of pk:
    def get_object(self, queryset=None):
        return Project.objects.get(pk=self.kwargs.get('project_id'))
    
def manual_team_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    colaboradores = User.objects.filter(role='collaborator')
    if request.method == 'POST':
        form = ManualTeamForm(request.POST)
        form.fields['members'].queryset = colaboradores
        if form.is_valid():
            name = form.cleaned_data['name']
            num_members = int(form.cleaned_data['num_members'])
            members = form.cleaned_data['members']
            if not name.strip():
                form.add_error('name', "O nome da equipe é obrigatório.")
            if not (3 <= members.count() <= 10):
                form.add_error('members', "Selecione entre 3 e 10 colaboradores.")
            elif members.count() != num_members:
                form.add_error('members', f"Selecione exatamente {num_members} colaboradores.")
            if not form.errors:
                team = Team.objects.create(name=name, project=project)
                # Crie um TeamAssignment para cada membro selecionado
                for member in members:
                    TeamAssignment.objects.create(team=team, user=member, role='Collaborator')
                messages.success(request, f"Equipe '{name}' criada com sucesso!")
                return redirect('project_detail', pk=project.pk)
    else:
        form = ManualTeamForm()
        form.fields['members'].queryset = colaboradores
    return render(request, 'projects/manual_team_create.html', {
        'form': form,
        'colaboradores': colaboradores,
        'project': project,
    })

def generate_team_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    collaborators = list(User.objects.filter(role='collaborator'))
    min_size, max_size = 3, 10

    if request.method == 'POST':
        member_ids = request.POST.getlist('members')
        team_name = request.POST.get('team_name')
        mode = request.POST.get('mode')
        if not member_ids or not team_name or mode != 'auto':
            messages.error(request, "Dados inválidos para criação automática.")
            return redirect('generate_team', project_id=project.id)
        if not (min_size <= len(member_ids) <= max_size):
            messages.error(request, f"Selecione entre {min_size} e {max_size} membros.")
            return redirect('generate_team', project_id=project.id)
        # Cria o time e associa membros
        team = Team.objects.create(name=team_name, project=project)
        for member_id in member_ids:
            user = User.objects.get(id=member_id)
            TeamAssignment.objects.create(team=team, user=user, role='Collaborator')
        messages.success(request, f"Equipe '{team_name}' criada com sucesso!")
        return redirect('project_detail', pk=project.pk)

    # GET: gera sugestão automática
    suggested_team = generate_balanced_team(collaborators, min_size, max_size)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    default_team_name = f"Team {project.id}-{timestamp}"
    return render(request, 'projects/generate_team.html', {
        'project': project,
        'suggested_team': suggested_team,
        'default_team_name': default_team_name,
        'min_size': min_size,
        'max_size': max_size,
    })