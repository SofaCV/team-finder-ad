import json

from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Project
from users.models import Skill, User


class UserModelTests(TestCase):
    def test_create_user_generates_avatar_and_phone(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="password",
            name="Иван",
            surname="Петров",
        )
        self.assertTrue(user.avatar)
        self.assertTrue(user.phone)
        self.assertEqual(user.name, "Иван")

    def test_phone_normalization_in_form(self):
        user = User.objects.create_user(
            email="phone@example.com",
            password="password",
            name="Анна",
            surname="Смирнова",
            phone="+79001234567",
        )
        self.client = Client()
        self.client.force_login(user)
        response = self.client.post(
            "/users/edit-profile/",
            {
                "name": "Анна",
                "surname": "Смирнова",
                "about": "",
                "phone": "89001234568",
                "github_url": "",
            },
        )
        user.refresh_from_db()
        self.assertEqual(user.phone, "+79001234568")


class RegistrationLoginTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_and_login(self):
        response = self.client.post(
            "/users/register/",
            {
                "name": "Мария",
                "surname": "Иванова",
                "email": "maria@yandex.ru",
                "password": "password",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="maria@yandex.ru").exists())

        response = self.client.post(
            "/users/login/",
            {"email": "maria@yandex.ru", "password": "password"},
        )
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            "/users/login/",
            {"email": "wrong@example.com", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Неверный имейл или пароль")


class SkillsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="skills@example.com",
            password="password",
            name="Пётр",
            surname="Сидоров",
            phone="+79001112233",
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_skills_autocomplete(self):
        Skill.objects.create(name="Python")
        Skill.objects.create(name="PostgreSQL")
        response = self.client.get("/users/skills/?q=P")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        names = [item["name"] for item in data]
        self.assertEqual(names, ["PostgreSQL", "Python"])

    def test_add_and_remove_skill(self):
        response = self.client.post(
            f"/users/{self.user.id}/skills/add/",
            data=json.dumps({"name": "React"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["created"])
        self.assertTrue(data["added"])
        skill_id = data["skill_id"]

        response = self.client.post(
            f"/users/{self.user.id}/skills/{skill_id}/remove/",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.skills.filter(pk=skill_id).exists())


class ParticipantsFilterTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="u1@example.com",
            password="password",
            name="А",
            surname="Б",
            phone="+79001111111",
        )
        self.user2 = User.objects.create_user(
            email="u2@example.com",
            password="password",
            name="В",
            surname="Г",
            phone="+79002222222",
        )
        skill = Skill.objects.create(name="Java")
        self.user1.skills.add(skill)

    def test_filter_by_skill(self):
        client = Client()
        response = client.get("/users/list/?skill=Java")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "А Б")
        self.assertNotContains(response, "В Г")
