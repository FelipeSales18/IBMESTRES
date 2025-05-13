from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('sucesso/', views.funcionario_sucesso, name='funcionario_sucesso'),
    path('funcionarios/', views.listar_funcionarios, name='listar_funcionarios'),  # Rota para listar funcionários
    path('equipes/', views.listar_equipes, name='listar_equipes'),  # Certifique-se de que esta rota existe
    path('equipe/<int:equipe_id>/', views.detalhes_equipe, name='detalhes_equipe'),
    path('associar-equipe/', views.associar_equipe, name='associar_equipe'),
    path('listar-associacoes/', views.listar_associacoes, name='listar_associacoes'),
    path('projetos/', views.listar_projetos, name='listar_projetos'),
    path('projetos/criar/', views.criar_projeto, name='criar_projeto'),
]