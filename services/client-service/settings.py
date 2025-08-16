INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://client:3000"
]
