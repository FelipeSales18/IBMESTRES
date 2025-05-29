from django.urls import path
from .views import (
    RegisterTypeSelectView, CollaboratorRegisterView, TeamLeaderRegisterView,
    UserLoginView, UserLogoutView, UserProfileView, team_leader_dashboard, collaborator_dashboard, edit_profile,
    ExternalPORegisterView,
)

urlpatterns = [
    path('register/', RegisterTypeSelectView.as_view(), name='register_select'),
    path('register/collaborator/', CollaboratorRegisterView.as_view(), name='register_collaborator'),
    path('register/team-leader/', TeamLeaderRegisterView.as_view(), name='register_team_leader'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='profile'),
    path('dashboard/', collaborator_dashboard, name='collaborator_dashboard'),
    path('dashboard/leader/', team_leader_dashboard, name='team_leader_dashboard'),
    path('profile/edit/', edit_profile, name='edit-profile'),
    path('register/external-po/', ExternalPORegisterView.as_view(), name='register_external_po'),
]