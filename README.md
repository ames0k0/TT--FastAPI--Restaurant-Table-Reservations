# Restaurant Table Reservations

API-сервис бронирования столиков в ресторане - [ТЗ](./_readme/TestTask.pdf)

### Скачивание проекта
```bash
git clone \
  --single-branch \
  --depth=1 \
  https://github.com/ames0k0/TT--FastAPI--Restaurant-Table-Reservations

cd TT--FastAPI--Restaurant-Table-Reservations
```

### Запуск проекта (Docker Compose)
<details>
  <summary>Зависимости</summary>
  <pre>docker -v  # Docker version 27.5.1, build 9f9e405</pre>
</details>

<details>
  <summary>Разработка и Тестирование</summary>

  ```bash
  # Database
  docker compose -f dev-docker-compose.yml up -d

  # Env variables
  export DB__POSTGRES_DSN=postgresql+psycopg2://postgres:simple@localhost:5454/restaurant_table_reservations
  export UVICORN__RELOAD=1

  # Sync dependencies
  uv sync

  # Start tests
  uv run pytest tests

  # Start an application
  uv run python main.py
  ```
</details>

```bash
docker compose up -d --build
```
| Сервис                        | Документация / SwaggerUI                  |
| ----------------------------- | ----------------------------------------- |
| http://localhost:8800/        | http://localhost:8800/docs                |


### Эндпоинты
#### Столики
- <details>
  <summary><strong>POST /tables</strong> - Создаёт нового столика</summary>

  | Тело запроса    | Тип    | Описание        | Пример     |
  | --------------- | ------ | --------------- | ---------- |
  | name            | Строка | Название стола  | Table 1    |
  | seats           | Число  | Количество мест | 2          |
  | location        | Строка | Положение стола | Зал у окна |

  ```bash
  curl -X 'POST' \
    'http://localhost:8800/tables/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "Table 1",
    "seats": 2,
    "location": "Зал у окна"
  }'
  ```

  ```json
  {
    "name": "Table 1",
    "seats": 2,
    "location": "Зал у окна",
    "id": 1
  }
  ```
  </details>

- <details>
  <summary><strong>GET /tables</strong> - Возвращает список всех столиков</summary>

  ```bash
  curl -X 'GET' \
    'http://localhost:8800/tables/' \
    -H 'accept: application/json'
  ```

  ```json
  [
    {
      "name": "Table 1",
      "seats": 2,
      "location": "Зал у окна",
      "id": 1
    }
  ]
  ```

- <details>
  <summary><strong>DELETE /tables/{id}</strong> - Удаляет столика по `id`</summary>

  | Параметры пути запроса | Тип    | Описание   | Пример |
  | ---------------------- | ------ | ---------- | ------ |
  | id                     | Число  | Айди стола | 1      |

  ```bash
  curl -X 'DELETE' \
    'http://localhost:8800/tables/1' \
    -H 'accept: application/json'
  ```

  ```json
  null
  ```

#### Брони
- <details>
  <summary><strong>POST /reservations/</strong> - Создаёт бронь</summary>

  | Тело запроса     | Тип    | Описание                          | Пример              |
  | ---------------- | ------ | --------------------------------- | ------------------- |
  | customer_name    | Строка | Имя клиента                       | Alice               |
  | reservation_time | Строка | Время брони                       | 2026-12-26 17:02:30 |
  | duration_minutes | Число  | Продолжительность брони в минутах | 120                 |
  | table_id         | Число  | Айди столика                      | 1                   |

  ```bash
  curl -X 'POST' \
    'http://localhost:8800/reservations/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "customer_name": "Alice",
    "reservation_time": "2026-12-26 17:02:30",
    "duration_minutes": 120,
    "table_id": 1
  }'
  ```

  ```json
  {
    "customer_name": "Alice",
    "reservation_time": "2026-12-26T17:02:30",
    "duration_minutes": 120,
    "table_id": 1,
    "id": 1
  }
  ```
  </details>

- <details>
  <summary><strong>GET /reservations/</strong> - Возвращает список всех броней</summary>

  ```bash
  curl -X 'GET' \
    'http://localhost:8800/reservations/' \
    -H 'accept: application/json'
  ```

  ```json
  [
    {
      "customer_name": "Alice",
      "reservation_time": "2026-12-26T17:02:30",
      "duration_minutes": 120,
      "table_id": 1,
      "id": 1
    }
  ]
  ```

- <details>
  <summary><strong>DELETE /reservations/{id}</strong> - Удаляет бронь по `id`</summary>

  | Параметры пути запроса | Тип    | Описание   | Пример |
  | ---------------------- | ------ | ---------- | ------ |
  | id                     | Число  | Айди брони | 1      |

  ```bash
  curl -X 'DELETE' \
    'http://localhost:8800/reservations/1' \
    -H 'accept: application/json'
  ```

  ```json
  null
  ```

### Остановка проекта и удаление
- Docker-образов, Docker-контейнеров, Хранилище, Сети
```bash
docker compose down --volumes --rmi local
```

<details>
<summary>Использованные технологии</summary>

| Название       | Ссылка                            |
| -------------- | --------------------------------- |
| FastApi        | https://fastapi.tiangolo.com/     |
| SQLModel       | https://sqlmodel.tiangolo.com/    |
| Pydantic       | https://docs.pydantic.dev/latest  |
| Uvicorn        | https://www.uvicorn.org/          |
| HTTPX          | https://www.python-httpx.org/     |
| pytest         | https://docs.pytest.org/en/stable |
| PostgreSQL     | https://www.postgresql.org        |
| Docker         | https://docs.docker.com           |
| Docker Compose | https://docs.docker.com/compose   |

</details>

---

<p align="center">
  <img src="./_readme/rest-api.png" />
  <img src="./_readme/Diagram.drawio.png" />
</p>
