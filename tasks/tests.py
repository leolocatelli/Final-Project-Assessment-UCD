from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Task, Category

class TaskModelTest(TestCase):

    def setUp(self):
        """Criação de um usuário e uma categoria para os testes"""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Work")

    def test_create_task(self):
        """Testa se uma tarefa pode ser criada corretamente"""
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            due_date=timezone.now() + timezone.timedelta(days=3),
            completed=False,
            user=self.user,
            category=self.category
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task.")
        self.assertEqual(task.completed, False)
        self.assertEqual(task.user.username, "testuser")

    def test_is_delayed_property(self):
        """Testa se a propriedade is_delayed retorna True para tarefas atrasadas"""
        task = Task.objects.create(
            title="Delayed Task",
            description="This task should be delayed.",
            due_date=timezone.now() - timezone.timedelta(days=1),  # Data no passado
            completed=False,
            user=self.user,
            category=self.category
        )
        self.assertTrue(task.is_delayed)

    def test_task_string_representation(self):
        """Testa se a string da tarefa retorna o título corretamente"""
        task = Task.objects.create(
            title="String Test Task",
            description="Testing string representation.",
            due_date=timezone.now(),
            completed=False,
            user=self.user,
            category=self.category
        )
        self.assertEqual(str(task), "String Test Task")
