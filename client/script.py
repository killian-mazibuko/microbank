from users.models import User
User.objects.create_superuser(
    username="admin",
    email="admin@example.com",
    password="AdminPass123!"
)
