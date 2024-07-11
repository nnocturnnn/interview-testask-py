from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.finance import router
from app.core.config import settings
from app.db import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(
    title=settings.APP_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

def create_app() -> FastAPI:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app.include_router(router, prefix=settings.API_V1_STR)

app = create_app()


