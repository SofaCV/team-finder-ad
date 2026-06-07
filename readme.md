# TeamFinder

Веб-приложение для поиска команды и pet-проектов. Реализован **вариант 2** (навыки пользователей и фильтрация участников по навыкам).

## Быстрый старт для ревьюера

### 1. Виртуальное окружение

```bash
python -m venv venv
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 2. Настройка `.env`

Скопируйте пример и заполните переменные:

```bash
cp .env_example .env
```

| Переменная | Назначение |
|------------|------------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django |
| `DJANGO_DEBUG` | `True` для разработки |
| `POSTGRES_*` | Параметры подключения к PostgreSQL |
| `TASK_VERSION` | `2` — шаблоны из `templates_var2` |
| `USE_SQLITE` | `True` — SQLite вместо PostgreSQL (только для локальной разработки без Docker) |

> **Для проверки по заданию** используйте PostgreSQL: запустите Docker (шаг 3) и **не указывайте** `USE_SQLITE` в `.env`.

### 3. Запуск PostgreSQL (Docker)

```bash
docker compose up -d
```

Остановка:
```bash
docker compose down
```

### 4. Миграции и тестовые данные

```bash
python manage.py migrate
python manage.py load_test_data
```

Команда `load_test_data` создаёт пользователей и проекты для проверки.

**Тестовый аккаунт:**
- Email: `maria@yandex.ru`
- Пароль: `password`

**Суперпользователь** (создать вручную):
```bash
python manage.py createsuperuser
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

Приложение доступно по адресу: [http://localhost:8000](http://localhost:8000)

Главная страница перенаправляет на `/projects/list/`.

### 6. Автотесты

```bash
python manage.py test
```

Тесты используют SQLite (настроено автоматически при запуске `test`).

## Структура проекта

| Приложение | Описание |
|------------|----------|
| `users` | Модели `User`, `Skill`; регистрация, авторизация, профиль, навыки |
| `projects` | Модель `Project`; список, детали, создание, участие, избранное |

## Реализованная функциональность

- Список проектов с пагинацией (12 на страницу)
- Регистрация, вход, выход, смена пароля
- Публичный профиль пользователя с навыками (добавление/удаление без перезагрузки)
- Фильтрация участников по навыкам (`/users/list/?skill=Python`)
- Создание и редактирование проектов
- Участие в проектах, завершение проекта автором
- Избранные проекты
- Админ-панель Django (`/admin/`) для управления пользователями и проектами

## API эндпоинты (JSON)

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/users/skills/?q=` | Автодополнение навыков |
| POST | `/users/<id>/skills/add/` | Добавить навык |
| POST | `/users/<id>/skills/<id>/remove/` | Удалить навык |
| POST | `/projects/<id>/complete/` | Завершить проект |
| POST | `/projects/<id>/toggle-participate/` | Участвовать/отказаться |
| POST | `/projects/<id>/toggle-favorite/` | Добавить/убрать из избранного |

## Проект выполняла Софья. 
## Моя почта: sofiadelf0608@rambler.ru
## Ссылка на мой GitHub: https://github.com/SofaCV
