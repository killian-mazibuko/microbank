import json, os
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_register_and_login(db):
    c = Client(HTTP_X_INTERNAL_TOKEN=os.environ.get("INTERNAL_TOKEN","changeme"))
    resp = c.post("/client/register", data=json.dumps({
        "username":"alice","email":"alice@example.com","password":"pw12345"
    }), content_type="application/json")
    assert resp.status_code == 201

    resp = c.post("/client/login", data=json.dumps({
        "username":"alice","password":"pw12345"
    }), content_type="application/json")
    assert resp.status_code == 200
    assert "token" in resp.json()
