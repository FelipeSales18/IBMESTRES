from django.test import TestCase
from .models import Team, TeamAssignment
from django.contrib.auth import get_user_model
User = get_user_model()

class TeamModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.team = Team.objects.create(name='Development Team', leader=self.user)

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Development Team')
        self.assertEqual(self.team.leader, self.user)

class TeamAssignmentModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.team = Team.objects.create(name='Development Team', leader=self.user1)
        self.assignment = TeamAssignment.objects.create(team=self.team, collaborator=self.user2)

    def test_team_assignment_creation(self):
        self.assertEqual(self.assignment.team, self.team)
        self.assertEqual(self.assignment.collaborator, self.user2)