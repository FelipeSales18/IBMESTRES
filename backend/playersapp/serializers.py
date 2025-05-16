# minhaapp/serializers.py
from rest_framework import serializers
from playersapp.models import Funcionario
from .models import Projeto, Team

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['nome', 'idade', 'hard_skils', 'soft_skils', 'ex_developer', 'ex_product_owner', 'ex_scrum_master']
        read_only_fields = ['id']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class ProjectSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    class Meta:
        model = Projeto
        fields = ['id', 'nome', 'descricao', 'data_criacao', 'team']