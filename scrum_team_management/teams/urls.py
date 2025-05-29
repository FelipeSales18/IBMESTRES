from django.urls import path
from . import views
from .views import collaborators_list_view

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team-list'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('create/', views.TeamCreateView.as_view(), name='team-create'),
    path('<int:pk>/update/', views.TeamUpdateView.as_view(), name='team-update'),
    path('<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team-delete'),
    path('collaborators/', collaborators_list_view, name='collaborators_list'),
    path('<int:pk>/assign-external-po/', views.assign_external_po, name='assign_external_po'),
]