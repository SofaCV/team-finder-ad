import json

from django.test import Client, TestCase

from projects.models import Project
from users.models import User


class ProjectTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="password",
            name="Олег",
            surname="Козлов",
            phone="+79003333333",
        )
        self.other = User.objects.create_user(
            email="other@example.com",
            password="password",
            name="Елена",
            surname="Новикова",
            phone="+79004444444",
        )
        self.project = Project.objects.create(
            name="Test Project",
            description="Описание",
            owner=self.owner,
            status="open",
        )
        self.project.participants.add(self.owner)
        self.client = Client()

    def test_project_list(self):
        response = self.client.get("/projects/list/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")

    def test_complete_project(self):
        self.client.force_login(self.owner)
        response = self.client.post(f"/projects/{self.project.id}/complete/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "closed")

    def test_toggle_participate(self):
        self.client.force_login(self.other)
        response = self.client.post(
            f"/projects/{self.project.id}/toggle-participate/"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["participant"])
        self.assertTrue(
            self.project.participants.filter(pk=self.other.pk).exists()
        )

    def test_toggle_favorite(self):
        self.client.force_login(self.other)
        response = self.client.post(
            f"/projects/{self.project.id}/toggle-favorite/"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["favorited"])

    def test_create_project(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            "/projects/create-project/",
            {
                "name": "Новый проект",
                "description": "Описание нового проекта",
                "github_url": "",
                "status": "open",
            },
        )
        self.assertEqual(response.status_code, 302)
        project = Project.objects.get(name="Новый проект")
        self.assertEqual(project.owner, self.owner)
        self.assertTrue(project.participants.filter(pk=self.owner.pk).exists())
