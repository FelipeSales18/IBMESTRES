from django.test import TestCase
from .models import Project

class ProjectModelTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
            description="A project for testing purposes."
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.description, "A project for testing purposes.")

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test Project")