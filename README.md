#### Development
```bash
# Database
docker compose up -d

# Env variables
export DB__POSTGRES_DSN=postgresql+psycopg2://postgres:simple@localhost:5454/restaurant_table_reservationsexport
export UVICORN__RELOAD=1

# Start an application
uv run python main.py
```