.PHONY: up down build logs migrate seed dev-backend dev-frontend test-backend test-frontend

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec backend python scripts/seed.py

# --- Local (non-Docker) development ---
# Requires a local PostgreSQL instance matching backend/.env DATABASE_URL.

dev-backend:
	cd backend && python -m venv .venv && . .venv/Scripts/activate && pip install -e ".[dev]" && \
		alembic upgrade head && python scripts/seed.py && uvicorn app.main:app --reload

dev-frontend:
	cd frontend && npm install && npm run dev

test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm run test
