from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Team, User
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