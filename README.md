# Task Tracker
Простий веб додаток для створення, редагування, керування та видалення задач

## Можливості
- Створення, перегляд, редагування та видалення задач
- Прості статуси задач (наприклад: todo / in-progress / done)
- Фільтрація/пошук

## Вимоги
- Python 3.10+ (рекомендовано)
- pip / venv (Docker в майбутньому)

## Встановлення

1) Клонуйте репозиторій
```bash
git clone https://github.com/fand1l/task_tracker.git
cd task_tracker
```

2) Створіть і активуйте віртуальне середовище
```bash
python -m venv .venv
```
macOS/Linux:
```bash
source .venv/bin/activate
```

3) Встановіть залежності
```bash
pip install -r requirements.txt
```

## Запуск
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Після запуску відкрийте в браузері:
```
http://localhost:8000
```

## Структура проєкту (приклад)
(in dev)