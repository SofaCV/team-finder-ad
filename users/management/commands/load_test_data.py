from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import Skill, User


class Command(BaseCommand):
    help = "Создаёт тестовых пользователей и проекты"

    def handle(self, *args, **options):
        maria, created = User.objects.get_or_create(
            email="maria@yandex.ru",
            defaults={
                "name": "Мария",
                "surname": "Петрова",
                "phone": "+79001234567",
                "about": "Python-разработчик, ищу команду для pet-проектов",
            },
        )
        if created:
            maria.set_password("password")
            maria.save()
            self.stdout.write("Создан пользователь maria@yandex.ru")
        else:
            maria.set_password("password")
            maria.save()
            self.stdout.write("Обновлён пароль maria@yandex.ru")

        users_data = [
            ("ivan@example.com", "Иван", "Сидоров", "+79001111111"),
            ("anna@example.com", "Анна", "Козлова", "+79002222222"),
            ("petr@example.com", "Пётр", "Новиков", "+79003333333"),
        ]
        users = [maria]
        for email, name, surname, phone in users_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"name": name, "surname": surname, "phone": phone},
            )
            if created:
                user.set_password("password")
                user.save()
            users.append(user)

        skills = ["Python", "Django", "JavaScript", "React", "PostgreSQL"]
        skill_objs = []
        for name in skills:
            skill, _ = Skill.objects.get_or_create(name=name)
            skill_objs.append(skill)

        maria.skills.set([skill_objs[0], skill_objs[1]])
        users[1].skills.set([skill_objs[0], skill_objs[4]])
        users[2].skills.set([skill_objs[2], skill_objs[3]])
        users[3].skills.set([skill_objs[1], skill_objs[4]])

        projects_data = [
            (maria, "TeamFinder Clone", "Клон платформы для поиска команды"),
            (users[1], "ML Dashboard", "Дашборд для машинного обучения"),
            (users[2], "React Game", "Браузерная игра на React"),
            (users[3], "API Gateway", "Микросервисный API Gateway"),
        ]
        for owner, name, description in projects_data:
            project, created = Project.objects.get_or_create(
                name=name,
                owner=owner,
                defaults={"description": description, "status": "open"},
            )
            if created:
                project.participants.add(owner)

        self.stdout.write(self.style.SUCCESS("Тестовые данные загружены"))
