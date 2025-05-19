from django.urls import path
from . import views
from .views import meu_perfil, minhas_equipes
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar_funcionario, name='cadastrar_colaborador'),
    path('sucesso/', views.funcionario_sucesso, name='funcionario_sucesso'),
    path('equipes/', views.EquipeListView.as_view(), name='listar_equipes'),
    path('equipe/<int:equipe_id>/', views.detalhes_equipe, name='detalhes_equipe'),
    path('associar-equipe/', views.associar_equipe, name='associar_equipe'),
    path('listar-associacoes/', views.listar_associacoes, name='listar_associacoes'),
    path('projetos/', views.listar_projetos, name='listar_projetos'),
    path('projetos/criar/', views.criar_projeto, name='criar_projeto'),
    path('meu-perfil/', meu_perfil, name='meu_perfil'),
    path('minhas-equipes/', minhas_equipes, name='minhas_equipes'),
    path('colaboradores/', views.listar_funcionarios, name='listar_colaboradores'),  # Rota para listar colaboradores
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)