from django.urls import path
from . import views
from .views import cadastrar_funcionario
from .views import funcionario_sucesso

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', cadastrar_funcionario, name='cadastrar_funcionario'),
    path('cadastro-sucesso/', funcionario_sucesso, name='funcionario_sucesso'),
]