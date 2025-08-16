FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD sh -c "python manage.py migrate && python manage.py seed_admin && gunicorn client_service.wsgi:application --bind 0.0.0.0:8000 --workers 3"
# After migrations
RUN python manage.py migrate
RUN python manage.py seed_admin