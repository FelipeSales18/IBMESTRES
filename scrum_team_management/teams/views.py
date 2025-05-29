from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST

from .models import Team, TeamAssignment
from users.models import User
from .forms import TeamForm

class TeamLeaderRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'team_leader'

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = context['team']
        assignments = team.teamassignment_set.select_related('user').all()
        context['team_leader'] = assignments.filter(role="Team Leader").first()
        context['product_owners'] = assignments.filter(role__in=["Internal PO", "External PO"])
        context['developers'] = assignments.filter(role="Developer")
        context['testers'] = assignments.filter(role="Tester")
        # Adicione todos os membros
        context['all_members'] = [a.user for a in assignments]
        context['external_pos'] = User.objects.filter(role='external_po')
        return context

class TeamCreateView(LoginRequiredMixin, TeamLeaderRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/create_team.html'
    success_url = reverse_lazy('team-list')

class TeamUpdateView(LoginRequiredMixin, TeamLeaderRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/edit_team.html'
    success_url = reverse_lazy('team-list')

class TeamDeleteView(LoginRequiredMixin, TeamLeaderRequiredMixin, DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('team-list')

@login_required
@user_passes_test(lambda u: u.role == 'team_leader')
def collaborators_list_view(request):
    collaborators = User.objects.filter(role='collaborator')
    return render(request, 'users/collaborators_list.html', {'collaborators': collaborators})

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    external_pos = User.objects.filter(role='external_po')
    context = {
        'team': team,
        'external_pos': external_pos
    }
    return render(request, 'teams/team_detail.html', context)

@require_POST
@login_required
def assign_external_po(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.user.role != 'team_leader':
        return redirect('team-detail', pk=pk)
    external_po_id = request.POST.get('external_po_id')
    if external_po_id:
        user = get_object_or_404(User, pk=external_po_id, role='external_po')
        # Remove any existing External PO
        team.teamassignment_set.filter(role="External PO").delete()
        # Assign new one
        TeamAssignment.objects.create(team=team, user=user, role="External PO")
    return redirect('team-detail', pk=pk)