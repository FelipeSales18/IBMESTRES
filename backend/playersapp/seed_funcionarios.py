import os
import sys
import django
import random
from faker import Faker

# Add the project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from playersapp.models import Funcionario  # ajuste se o nome da model for diferente

fake = Faker('pt_BR')  # localiza em português brasileiro

hard_skills_list = ['Python', 'Java', 'SQL', 'React', 'Django']
soft_skills_list = ['Comunicação', 'Liderança', 'Trabalho em equipe']
experiencias = ['Sim', 'Não']

# Map "Sim" and "Não" to True and False
experiencias_map = {'Sim': True, 'Não': False}

for _ in range(50):
    Funcionario.objects.create(
        nome=fake.name(),
        idade=random.randint(20, 60),
        hard_skils=random.choice(hard_skills_list),
        soft_skils=random.choice(soft_skills_list),
        ex_developer=experiencias_map[random.choice(experiencias)],
        ex_product_owner=experiencias_map[random.choice(experiencias)],
        ex_scrum_master=experiencias_map[random.choice(experiencias)]
    )

print("Funcionários criados com sucesso!")
