from django.urls import path
from . import views
from .views import manual_team_create, add_team_to_project, add_project_update

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('<int:project_id>/confirmation/', views.ProjectConfirmationView.as_view(), name='project_confirmation'),
    path('<int:project_id>/create-team-manually/', views.manual_team_create, name='manual_team_create'),
    path('<int:project_id>/generate-team/', views.generate_team_view, name='generate_team'),
    path('<int:project_id>/manual_team_create/', manual_team_create, name='manual_team_create'),
    path('<int:project_id>/add-team/', add_team_to_project, name='add_team_to_project'),
    path('<int:project_id>/remove_team/', views.remove_team_from_project, name='remove_team_from_project'),
    path('<int:project_id>/add_update/', add_project_update, name='add_project_update'),
    path('<int:project_id>/updates/', views.project_updates_list, name='project_updates_list'),
    path('<int:pk>/edit_testers/', views.edit_project_testers, name='edit_project_testers'),
    path('project/<int:pk>/add_tester/', views.add_project_tester, name='add_project_tester'),
    path('project/<int:pk>/remove_tester/<int:tester_pk>/', views.remove_project_tester, name='remove_project_tester'),
]