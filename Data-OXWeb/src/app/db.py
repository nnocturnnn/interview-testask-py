from app.core.config import settings


TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URI},
    "apps": {
        "models": {
            "models": ["app.api.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
