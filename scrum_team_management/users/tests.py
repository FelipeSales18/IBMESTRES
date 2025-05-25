from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='collaborator'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_user_role(self):
        self.assertEqual(self.user.role, 'collaborator')

    def test_team_leader_role(self):
        team_leader = User.objects.create_user(
            username='teamleader',
            password='leaderpassword',
            role='team_leader'
        )
        self.assertEqual(team_leader.role, 'team_leader')