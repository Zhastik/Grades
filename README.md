## Features
  - `POST /upload-grades` — загрузка CSV, валидация, сохранение в PostgreSQL:
  - `GET /students/more-than-3-twos` — студенты, у которых оценка 2 встречается больше 3 раз
  - `GET /students/less-than-5-twos` — студенты, у которых оценка 2 встречается меньше 5 раз

Миграции через Alembic

## Install
```bash
git clone https://github.com/Zhastik/Grades
```
```bash
Grades
```

## Start  
Установка зависимостей
```bash
pip install -r requirements.txt
```

Создание бд
```psql
CREATE DATABASE grades_db;
CREATE USER grades_user WITH PASSWORD 'grades_pass';
GRANT ALL PRIVILEGES ON DATABASE grades_db TO grades_user;
```

Если alembic будет ругать на права доступа
```psql
GRANT USAGE, CREATE ON SCHEMA public TO grades_user;
```

Переменные окружения
```
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="grades_db"
$env:DB_USER="grades_user"
$env:DB_PASS="grades_pass"
```

Миграции Alembic
```bash
alembic upgrade head
```

Запуск
```bash
uvicorn app.main:app --reload
```

## Start через Docker 
Запуск через Docker Compose
```bash
docker compose up --build
```
`API:` http://localhost:8000
`Swagger:` http://localhost:8000/docs

