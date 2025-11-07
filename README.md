# Scrum Team Management / Aplicativo de Gestão de Equipes SCRUM

Português / Português-BR
-----------------------

Resumo
-----
Aplicação Django para gerenciar projetos SCRUM, equipes e papéis (Team Leader, Collaborator, External PO). Fornece criação de projetos, atribuição de equipes e controle de acesso por função.

Recursos Principais
-------------------
- Gerenciamento de usuários com papéis (Líder de Equipe, Colaborador, PO Externo).
- Criação e acompanhamento de projetos.
- Criação manual e geração automática de equipes.
- Atualizações de projetos (o que foi feito, andamento, dificuldades).
- Interfaces administrativas via Django Admin.

Instalação Rápida
-----------------
1. Clone o repositório:
   git clone <repository-url>
   cd scrum_team_management

2. Instale dependências:
   pip install -r requirements.txt

3. Execute migrações:
   python manage.py migrate

4. Crie um superusuário:
   python manage.py createsuperuser

5. Rode o servidor de desenvolvimento:
   python manage.py runserver

Acessando
--------
Abra http://127.0.0.1:8000/ no navegador.

Estrutura do Projeto (selecionado)
----------------------------------
- [manage.py](manage.py) - utilitário de gerenciamento.
- [requirements.txt](requirements.txt) - dependências do projeto.
- [scrum_team_management/](scrum_team_management/) - configurações do projeto (ex.: [scrum_team_management/scrum_team_management/settings.py](scrum_team_management/scrum_team_management/settings.py)).
- [projects/](scrum_team_management/projects/) - app de projetos.
- [teams/](scrum_team_management/teams/) - app de equipes.
- [users/](scrum_team_management/users/) - app de usuários.
- [LICENSE](LICENSE) - licença do projeto (MIT).

Contribuindo
------------
- Abra issues para bugs ou melhorias.
- Faça fork / branch / PR com testes e descrição clara.
- Mantenha o padrão de estilo do projeto.

Contato
-------
Use o sistema de issues do repositório.

English / Inglês
----------------

Overview
--------
Django application to manage SCRUM projects, teams and roles (Team Leader, Collaborator, External PO). Supports project creation, team assignment (manual or generated) and role-based access control.

Key Features
------------
- User roles management (Team Leader, Collaborator, External PO).
- Project creation and updates.
- Manual and automatic team generation.
- Project updates: what was done, how it's going, setbacks.
- Admin interface via Django Admin.

Quickstart
----------
1. Clone the repo:
   git clone <repository-url>
   cd scrum_team_management

2. Install dependencies:
   pip install -r requirements.txt

3. Apply migrations:
   python manage.py migrate

4. Create a superuser:
   python manage.py createsuperuser

5. Run the development server:
   python manage.py runserver

Access
------
Open http://127.0.0.1:8000/ in your browser.

Project Layout (selected)
-------------------------
- [manage.py](manage.py)
- [requirements.txt](requirements.txt)
- [scrum_team_management/](scrum_team_management/) (see [scrum_team_management/scrum_team_management/settings.py](scrum_team_management/scrum_team_management/settings.py))
- [projects/](scrum_team_management/projects/)
- [teams/](scrum_team_management/teams/)
- [users/](scrum_team_management/users/)
- [LICENSE](LICENSE)

Contributing
------------
- File issues for bugs/improvements.
- Fork → branch → PR, include tests and clear description.
- Follow existing code style.

License
-------
MIT License — see [LICENSE](LICENSE).