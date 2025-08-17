# Microbank: A Full-Stack Microservice Banking Platform

A simple microservice-based banking demo with:

- **Client Service** (Django REST Framework): registration, login (JWT), profile, admin blacklisting
- **Banking Service** (Django REST Framework): deposits, withdrawals, balance & transactions
- **Nginx** API Gateway (+ internal service-to-service token)
- **RabbitMQ** for async blacklisting propagation
- **Next.js/React** client app (client dashboard & admin panel)
- **SQLite** databases stored under `/data` inside the containers, mapped to Docker volumes
- **Swagger/OpenAPI** via drf-spectacular at `/api/docs`
- **Rate limiting** for sensitive endpoints
- **Unit tests** for critical flows
- **wait-for-it.sh** to ensure services are up before Nginx starts
- **Docker Compose** to orchestrate everything

## Repo Layout

```
/client                            # Next.js frontend (client + admin UI)
/services/client-service           # DRF app for clients
/services/banking-service          # DRF app for banking
/nginx                             # API gateway config + wait-for-it.sh
/docker-compose.yml
/.env.example
```

3. Open:
   - Frontend: http://20.63.49.65:3000
   - Client Service docs: http://20.63.49.65:8001/api/docs
   - Banking Service docs: http://20.63.49.65:8002/api/docs
   - Nginx Gateway (APIs): http://20.63.49.65:8080
   - RabbitMQ Management (guest/guest): http://20.63.49.65:15672

### Default Admin

- Email: `admin@example.com`
- Password: `AdminPass123!`

Created on first run in both services via environment variables.

6. **Access**:
   - Next.js client: `http://20.63.49.65:3000`
   - API Gateway: `http://20.63.49.65:8080`
   - RabbitMQ mgmt: `http://20.63.49.65:15672` (guest/guest)

## Security Notes

- Uses JWT (HS256) with a shared secret across services.
- Nginx injects `X-Internal-Token` to backend services; services validate this header for an additional service-to-service trust layer.
- DRF throttling protects sensitive endpoints.
- Blacklisting is propagated asynchronously via RabbitMQ; banking service consumes updates and blocks blacklisted users.
- Databases live under `/data` in each container, mapped to durable Docker volumes (no local file paths).

## Tests

Run inside each service container:

```bash
docker compose exec client-service pytest
docker compose exec banking-service pytest
```

## Postman / OpenAPI

- Swagger UI per service at `/api/docs`
- Raw schema: `/api/schema`

Project By Killian T. Mazibuko
