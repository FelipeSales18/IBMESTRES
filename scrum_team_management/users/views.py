from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import CollaboratorRegisterForm, TeamLeaderRegisterForm, UserEditForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from projects.models import Project
from teams.models import Team

User = get_user_model()


@login_required
def collaborator_dashboard(request):
    user = request.user
    # Get teams the user is assigned to
    teams = Team.objects.filter(
        id__in=user.teamassignment_set.values_list('team_id', flat=True)
    )
    # Get projects related to those teams
    projects = Project.objects.filter(
        teams__in=teams
    ).distinct()
    return render(request, 'users/collaborator_dashboard.html', {
        'teams': teams,
        'projects': projects,
    })

@login_required
def team_leader_dashboard(request):
    user = request.user
    # Projects where the user is the team leader
    projects = Project.objects.filter(team_leader=user)
    # Teams related to those projects
    teams = Team.objects.filter(project__in=projects)
    return render(request, 'users/team_leader_dashboard.html', {
        'teams': teams,
        'projects': projects,
    })

class RegisterTypeSelectView(View):
    def get(self, request):
        return render(request, 'users/register_select.html')

class CollaboratorRegisterView(View):
    def get(self, request):
        form = CollaboratorRegisterForm()
        return render(request, 'users/register_collaborator.html', {'form': form})

    def post(self, request):
        form = CollaboratorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            # Redirect to appropriate dashboard
            return redirect('collaborator_dashboard')
        return render(request, 'users/register_collaborator.html', {'form': form})

class TeamLeaderRegisterView(View):
    def get(self, request):
        form = TeamLeaderRegisterForm()
        return render(request, 'users/register_team_leader.html', {'form': form})

    def post(self, request):
        form = TeamLeaderRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'users/register_team_leader.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        if self.request.user.role == 'team_leader':
            return reverse_lazy('team_leader_dashboard')
        return reverse_lazy('collaborator_dashboard')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class UserProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    pk_url_kwarg = 'user_id'

@login_required
@user_passes_test(lambda u: u.role == 'team_leader')
def collaborators_list_view(request):
    collaborators = User.objects.filter(role='collaborator').order_by('-role', 'last_name', 'first_name')
    team_leaders = User.objects.filter(role='team_leader').order_by('last_name', 'first_name')
    users = list(team_leaders) + list(collaborators)
    return render(request, 'users/collaborators_list.html', {'collaborators': users})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.pk)
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})