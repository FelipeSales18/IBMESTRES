# minhaapp/serializers.py
from rest_framework import serializers
from playersapp.models import Funcionario

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['nome', 'idade', 'hard_skils', 'soft_skils', 'ex_developer', 'ex_product_owner', 'ex_scrum_master']
        read_only_fields = ['id']