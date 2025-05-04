from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('sucesso/', views.funcionario_sucesso, name='funcionario_sucesso'),
    path('funcionarios/', views.listar_funcionarios, name='listar_funcionarios'),  # Nova rota para listar funcionários
]