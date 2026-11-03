# Notes REST API Service

Учебный проект по созданию REST API сервиса для управления заметками с использованием Flask, SQLAlchemy и PostgreSQL/SQLite.

## Функционал
- **Пользователи**: Создание профилей пользователей.
- **Заметки (CRUD)**: Создание, чтение, обновление и удаление заметок.
- **Связанные таблицы**: Заметки привязаны к конкретным авторам (Foreign Key).
- **Фильтрация и пагинация**: Получение списка заметок с возможностью фильтрации по категории и пользователю.
- **Тесты**: Полное покрытие функционала с помощью `pytest`.

## Структура проекта
```
notes_api/
│
├── app/
│   ├── __init__.py      # Инициализация приложения и базы данных
│   ├── models.py        # SQLAlchemy модели (User, Note)
│   └── routes.py        # REST API эндпоинты (CRUD, фильтрация, пагинация)
├── tests/
│   ├── __init__.py
│   └── test_api.py      # Unit-тесты с pytest
├── Dockerfile           # Контейнеризация приложения
├── requirements.txt     # Зависимости Python
├── .env.example         # Пример переменных окружения
└── README.md            # Документация проекта
```

## Локальный запуск
1. Клонируйте репозиторий / распакуйте архив:
   ```bash
   cd notes_api
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите приложение:
   ```bash
   flask --app app run
   ```

## Запуск тестов
```bash
pytest
```

## Запуск через Docker
```bash
docker build -t notes-api .
docker run -p 5000:5000 notes-api
```

## Примеры API запросов (cURL)

### 1. Создать пользователя
```bash
curl -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{"username": "alex", "email": "alex@example.com"}'
```

### 2. Создать заметку
```bash
curl -X POST http://127.0.0.1:5000/notes \
-H "Content-Type: application/json" \
-d '{"title": "Первая заметка", "content": "Текст заметки...", "category": "study", "user_id": 1}'
```

### 3. Получить список заметок с фильтрацией и пагинацией
```bash
curl "http://127.0.0.1:5000/notes?category=study&page=1&per_page=5"
```
