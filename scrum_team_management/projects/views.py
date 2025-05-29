from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Project
from .forms import ProjectForm, ProjectUpdateForm
from teams.forms import ManualTeamForm
from teams.models import Team, TeamAssignment
from users.models import User

import random
from datetime import datetime

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # Exclude users already assigned to any team in this project
        assigned_user_ids = set(
            assignment.user_id
            for team in project.teams.all()
            for assignment in team.teamassignment_set.all()
        )
        collaborators = User.objects.filter(role='collaborator').exclude(id__in=assigned_user_ids)

        context.update({
            'project': project,
            'collaborators': collaborators,
            # ... other context ...
        })
        return context

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
    project_competencies = [c.strip().lower() for c in (project.preferred_competencies or '').splitlines() if c.strip()]
    team_leader = request.user
    # Get all user IDs already assigned to any team in this project
    assigned_user_ids = set(
        assignment.user_id
        for team in project.teams.all()
        for assignment in team.teamassignment_set.all()
    )

    # Only include collaborators not already assigned
    collaborators = User.objects.filter(role='collaborator').exclude(id__in=assigned_user_ids)

    # Helper: count how many project competencies the user has
    def competency_match_count(user):
        if not hasattr(user, 'roles_preferred') or not user.roles_preferred:
            return 0
        user_competencies = [c.strip().lower() for c in user.roles_preferred.split(',')]
        return sum(1 for pc in project_competencies if pc in user_competencies)

    # Sort collaborators: more matches first
    sorted_collaborators = sorted(
        collaborators,
        key=lambda user: competency_match_count(user),
        reverse=True
    )

    ids = [user.id for user in sorted_collaborators]

    if request.method == 'POST':
        form = ManualTeamForm(request.POST)
        form.fields['members'].queryset = User.objects.filter(id__in=ids)
        if form.is_valid():
            name = form.cleaned_data['name']
            num_members = int(form.cleaned_data['num_members'])
            members = form.cleaned_data['members']
            total_selected = members.count() + 3  # 3 required roles

            if not name.strip():
                form.add_error('name', "O nome da equipe é obrigatório.")
            if not (3 <= total_selected <= 10):
                form.add_error('members', "Selecione entre 3 e 10 membros (incluindo os obrigatórios).")
            elif total_selected != num_members:
                form.add_error('members', f"Selecione exatamente {num_members} membros (incluindo os obrigatórios).")
            if not form.errors:
                team = Team.objects.create(name=name, project=project)
                # Crie um TeamAssignment para cada membro selecionado
                for member in members:
                    TeamAssignment.objects.create(team=team, user=member, role='Collaborator')
                # Create TeamAssignment for Team Leader
                TeamAssignment.objects.create(team=team, user=team_leader, role='Team Leader')
                # Create TeamAssignment for Internal PO
                internal_po = User.objects.get(id=request.POST.get('internal_po'))
                TeamAssignment.objects.create(team=team, user=internal_po, role='Internal PO')
                # Create TeamAssignment for External PO
                external_po_id = request.POST.get('external_po')
                if external_po_id:
                    external_po = User.objects.get(id=external_po_id)
                    TeamAssignment.objects.create(team=team, user=external_po, role='External PO')
                messages.success(request, f"Equipe '{name}' criada com sucesso!")
                return redirect('project_detail', pk=project.pk)
    else:
        form = ManualTeamForm()
        form.fields['members'].queryset = User.objects.filter(id__in=ids)

    return render(request, 'projects/manual_team_create.html', {
        'form': form,
        'colaboradores': sorted_collaborators,
        'project': project,
        'team_leader': team_leader,
        'project_competencies': project_competencies,
    })

def generate_team_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    assigned_user_ids = set(
        assignment.user_id
        for team in project.teams.all()
        for assignment in team.teamassignment_set.all()
    )
    
    collaborators = list(
        User.objects.filter(role='collaborator').exclude(id__in=assigned_user_ids)
    )
    
    min_size, max_size = 4, 10

    # Helper functions for algorithms
    def greedy_team(collaborators, project_competencies, team_size):
        def score(user):
            # 1. Competency match count
            user_comp = [c.skill_name.strip().lower() for c in user.competencies.all()]
            competency_matches = len(set(user_comp) & set(project_competencies))

            # 2. Preferred role match (1 if matches, 0 if not)
            # We'll check if any of the user's preferred roles matches the required roles for the team
            # For simplicity, let's assume you want to prioritize Internal PO, External PO, Collaborator
            preferred_roles = [r.strip().lower() for r in (user.roles_preferred or '').split(',')]
            # You can adjust this list as needed
            required_roles = ['internal po', 'external po', 'collaborator']
            role_match = int(any(role in required_roles for role in preferred_roles))

            # 3. Years of experience
            years = getattr(user, 'years_of_experience', 0) or 0

            # Return a tuple for sorting: higher is better
            return (competency_matches, role_match, years)
        sorted_collabs = sorted(collaborators, key=score, reverse=True)
        return sorted_collabs[:team_size]

    def balanced_team(collaborators, project_competencies, team_size):
        selected = []
        used_competencies = set()
        for comp in project_competencies:
            for user in collaborators:
                user_comp = [c.skill_name.strip().lower() for c in user.competencies.all()]
                if comp in user_comp and user not in selected:
                    selected.append(user)
                    used_competencies.update(user_comp)
                    break
        for user in collaborators:
            user_comp = set([c.skill_name.strip().lower() for c in user.competencies.all()])
            if user not in selected and not user_comp.issubset(used_competencies):
                selected.append(user)
                used_competencies.update(user_comp)
            if len(selected) >= team_size:
                break
        if len(selected) < team_size:
            for user in collaborators:
                if user not in selected:
                    selected.append(user)
                if len(selected) >= team_size:
                    break
        return selected[:team_size]

    def random_team(collaborators, team_size):
        import random
        return random.sample(collaborators, min(team_size, len(collaborators)))

    project_competencies = [c.strip().lower() for c in (project.preferred_competencies or '').splitlines() if c.strip()]

    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        num_members = int(request.POST.get('num_members', 4))
        algorithm = request.POST.get('algorithm', 'balanced')

        # Exclude current user from pool
        pool = [u for u in collaborators if u != request.user]

        # Generate the rest of the team (N-1 members)
        team_size = num_members - 1
        if algorithm == 'greedy':
            generated_members = greedy_team(pool, project_competencies, team_size)
        elif algorithm == 'balanced':
            generated_members = balanced_team(pool, project_competencies, team_size)
        else:
            generated_members = random_team(pool, team_size)

        # Ensure enough members
        if len(generated_members) < team_size:
            messages.error(request, "Não foi possível selecionar membros suficientes para a equipe.")
            return redirect('generate_team', project_id=project.id)

        # Assign roles: current user = Team Leader, then Internal PO, External PO, rest Collaborators
        team = Team.objects.create(name=team_name, project=project)
        TeamAssignment.objects.create(team=team, user=request.user, role="Team Leader")
        # Do NOT include external_po users in this pool

        # When assigning roles, skip External PO
        for idx, member in enumerate(generated_members):
            if idx == 0:
                role = "Internal PO"
            # elif idx == 1:  # Remove this for External PO
            #     role = "External PO"
            else:
                role = "Collaborator"
            TeamAssignment.objects.create(team=team, user=member, role=role)
        messages.success(request, f"Equipe '{team_name}' criada com sucesso!")
        return redirect('project_detail', pk=project.pk)

    # GET: show form and suggested team
    default_team_name = f"Team {project.id}"
    suggested_team = []
    algorithm = request.GET.get('algorithm', 'greedy')
    num_members = int(request.GET.get('num_members', 4))
    pool = [u for u in collaborators if u != request.user]
    if algorithm == 'greedy':
        generated_members = greedy_team(pool, project_competencies, num_members - 1)
    elif algorithm == 'balanced':
        generated_members = balanced_team(pool, project_competencies, num_members - 1)
    else:
        generated_members = random_team(pool, num_members - 1)

    # For display: current user first, then generated members
    suggested_team = [request.user] + generated_members

    return render(request, 'projects/generate_team.html', {
        'project': project,
        'suggested_team': suggested_team,
        'default_team_name': default_team_name,
        'min_size': min_size,
        'max_size': max_size,
    })

def add_team_to_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    # Teams without a project assigned
    available_teams = Team.objects.filter(project__isnull=True)

    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        if team_id:
            team = get_object_or_404(Team, pk=team_id)
            team.project = project
            team.save()
            messages.success(request, f"Equipe '{team.name}' atribuída ao projeto!")
            return redirect('project_detail', pk=project.pk)
        # If no team selected, just reload the page (could add error handling)

    return render(request, 'projects/add_team_to_project.html', {
        'project': project,
        'available_teams': available_teams,
    })

@login_required
def remove_team_from_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        team_id = request.POST.get("team_id")
        if team_id:
            team = get_object_or_404(Team, pk=team_id, project=project)
            team.project = None
            team.save()
    return redirect('project_detail', pk=project_id)

@login_required
def add_project_update(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user != project.team_leader:
        return redirect('project_detail', pk=project_id)
    if request.method == 'POST':
        form = ProjectUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.project = project
            update.save()
            return redirect('project_detail', pk=project_id)
    else:
        form = ProjectUpdateForm()
    return render(request, 'projects/add_project_update.html', {'form': form, 'project': project})


def project_updates_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    updates = project.updates.order_by('-created_at')
    return render(request, 'projects/project_updates_list.html', {
        'project': project,
        'updates': updates,
    })


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.team_leader:
        return redirect('project_detail', pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'project': project})

@login_required
def edit_project_testers(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.team_leader:
        return redirect('project_detail', pk=pk)

    # Get all user IDs already assigned to any team in this project
    assigned_user_ids = set(
        assignment.user_id
        for team in project.teams.all()
        for assignment in team.teamassignment_set.all()
    )

    if request.method == 'POST':
        tester_ids = request.POST.getlist('testers')
        # Only allow collaborators not already assigned to the project
        testers = User.objects.filter(
            pk__in=tester_ids,
            role='collaborator'
        ).exclude(id__in=assigned_user_ids)
        project.testers.set(testers)
        project.save()
        return redirect('project_detail', pk=pk)
    return redirect('project_detail', pk=pk)

@login_required
def add_project_tester(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user == project.team_leader and request.method == "POST":
        tester_id = request.POST.get("tester")
        if tester_id:
            tester = get_object_or_404(User, pk=tester_id)
            if tester not in project.testers.all():
                project.testers.add(tester)
    return redirect('project_detail', pk=pk)

@login_required
def remove_project_tester(request, pk, tester_pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user == project.team_leader and request.method == "POST":
        tester = get_object_or_404(User, pk=tester_pk)
        project.testers.remove(tester)
    return redirect('project_detail', pk=pk)