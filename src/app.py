from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from starlette import status

from src.config import cors_config, URLPathsConfig, URLNamesConfig
from src.core.database.connection import DATABASE_URL
from src.core.database.base import Base
from src.users.router import router as users_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    """
    Runs events before application startup and after application shutdown.
    """

    # Startup events:
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown events:


app = FastAPI(lifespan=lifespan)

# Middlewares:
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ALLOW_ORIGINS,
    allow_credentials=cors_config.ALLOW_CREDENTIALS,
    allow_methods=cors_config.ALLOW_METHODS,
    allow_headers=cors_config.ALLOW_HEADERS,
)

# Routers:
app.include_router(users_router)


@app.get(
    path=URLPathsConfig.HOMEPAGE,
    response_class=RedirectResponse,
    name=URLNamesConfig.HOMEPAGE,
    status_code=status.HTTP_303_SEE_OTHER
)
async def homepage():
    return RedirectResponse(
        status_code=status.HTTP_303_SEE_OTHER,
        url=URLPathsConfig.DOCS
    )
