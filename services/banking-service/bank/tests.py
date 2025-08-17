import json, os
from django.test import Client

def auth_headers(token):
    return {
        "HTTP_X_INTERNAL_TOKEN": os.environ.get("INTERNAL_TOKEN","changeme"),
        "HTTP_AUTHORIZATION": f"Bearer {token}",
        "CONTENT_TYPE": "application/json",
    }

def test_health(db):
    c = Client()
    resp = c.get("/health/")
    assert resp.status_code == 200
