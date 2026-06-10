# Docker Setup

Build and run the API, Celery worker, PostgreSQL, and Redis:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

Stop the stack:

```bash
docker compose down
```

Remove local database and Redis volumes:

```bash
docker compose down -v
```
