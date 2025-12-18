## Features
  - `POST /upload-grades` — загрузка CSV, валидация, сохранение в PostgreSQL:
  - `GET /students/more-than-3-twos` — студенты, у которых оценка 2 встречается больше 3 раз
  - `GET /students/less-than-5-twos` — студенты, у которых оценка 2 встречается меньше 5 раз

Миграции через Alembic

## Install
```bash
git clone <repo-url>
```
```bash
cd <путь до папки>
```
```bash
pip install -r requirements.txt
```

## Start
Запуск через Docker Compose
```bash
docker compose up --build
```
`API:` http://localhost:8000
`Swagger:` http://localhost:8000/docs

