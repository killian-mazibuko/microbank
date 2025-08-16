# Microbank: A Full-Stack Microservice Banking Platform

This repository contains a minimal, production-leaning implementation of **Microbank** with two Django REST microservices, a Next.js/Tailwind frontend, an API gateway (Nginx), RabbitMQ for async blacklisting, and Docker Compose for orchestration.

## Services

- **Client Service** (`/services/client-service`): Registration/login (JWT), profile, admin client list, and blacklist toggle. Publishes blacklist events to RabbitMQ and exposes Swagger (OpenAPI) docs.
- **Banking Service** (`/services/banking-service`): Deposit/withdraw, balance + transactions, overdraft protection, local blacklist enforcement subscribed via RabbitMQ. Swagger (OpenAPI).
- **Frontend** (`/client`): Next.js client app with register/login, dashboard (balance & txn list), deposit/withdraw, and an admin panel to blacklist clients.
- **Gateway** (`/nginx`): API gateway that routes `/api/client/*` and `/api/banking/*` to the respective services and serves the frontend. Rate-limits sensitive endpoints.
- **RabbitMQ**: Message queue for async blacklist propagation.
- **PostgreSQL** (2 instances): One for each Django service.

## Quick Start (Local via Docker Compose)

1. **Copy envs** and adjust secrets as needed:
   ```bash
   cp services/client-service/.env.sample services/client-service/.env
   cp services/banking-service/.env.sample services/banking-service/.env
   cp client/.env.example client/.env.local
   ```
2. **Start** everything:
   ```bash
   docker compose up --build
   ```
3. **Access**:
   - Frontend: http://localhost/
   - Client API docs (Swagger UI): http://localhost/api/client/api/schema/swagger/
   - Banking API docs (Swagger UI): http://localhost/api/banking/api/schema/swagger/

### Default Admin

- Email: `admin@example.com`
- Password: `adminpass`

> Created automatically by the Client Service at startup for demo purposes. Toggle `CREATE_DEMO_ADMIN` in env to disable.

## Tech Notes

- **Auth**: JWT via `djangorestframework-simplejwt` with a shared `JWT_SECRET` across services.
- **Blacklist**: Admin toggles in Client Service publish messages (`client.blacklist` routing key) to RabbitMQ. Banking Service consumer updates a local blacklist table; all banking endpoints reject blacklisted clients.
- **Rate limiting**: Django REST throttles + Nginx `limit_req` on `/api/banking/deposit|withdraw` routes.
- **Service-to-service auth**: Protected internal endpoint `/api/internal/blacklist-dump/` on Client Service requiring an `X-Internal-Token`. Banking Service can run a one-time sync command on startup.
- **Swagger**: DRF Spectacular at `/api/schema/` and `/api/schema/swagger/` for both services.

## Exporting OpenAPI Specs

Inside each Django container:

```bash
python manage.py spectacular --file schema.yaml
```

The file will be emitted in the service working directory.

## Project Layout

```
/client                     # Next.js + Tailwind frontend
/nginx/nginx.conf           # API gateway
/services
  /client-service           # Django (DRF) Client Service
  /banking-service          # Django (DRF) Banking Service
docker-compose.yml
```

---
