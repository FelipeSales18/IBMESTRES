from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project
from .forms import ProjectForm

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
    
from django.http import HttpResponse

def create_team_manually_view(request, project_id):
    return HttpResponse("Manual team creation page coming soon.")

def generate_team_view(request, project_id):
    return HttpResponse("Team generation algorithm coming soon.")