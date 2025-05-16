# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Importação necessária para LogoutView
from accounts.views import ProjectListView
from playersapp.views import (
    EquipeListView, EquipeCreateView, EquipeUpdateView,
    EquipeDeleteView, EquipeDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('playersapp.urls')),  # Inclui as rotas do aplicativo playersapp
    path('register/', include('accounts.urls')),
    path('api/', include('playersapp.api_urls')),  # URLs da API
    path('api-auth/', include('rest_framework.urls')),  # Login para a API
    path("accounts/", include("django.contrib.auth.urls")),  # accounts
    path('projetos/', ProjectListView.as_view(), name='project-list'),
    path('equipes/', EquipeListView.as_view(), name='listar_equipes'),
    path('equipes/criar/', EquipeCreateView.as_view(), name='cadastrar_equipe'),
    path('equipes/<int:pk>/editar/', EquipeUpdateView.as_view(), name='editar_equipe'),
    path('equipes/<int:pk>/excluir/', EquipeDeleteView.as_view(), name='excluir_equipe'),
    path('equipes/<int:pk>/', EquipeDetailView.as_view(), name='detalhes_equipe'),
    # ... outras rotas ...
]