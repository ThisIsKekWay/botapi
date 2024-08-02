from contextlib import asynccontextmanager
from aioredis import Redis

from fastapi import FastAPI

from fastapi_versioning import VersionedFastAPI

from app.config import settings
from app.router import router as message_router

app = FastAPI(
    title="Просмотр сообщений",
    root_path="/api"
)
app.include_router(message_router)
app = VersionedFastAPI(
    app=app,
    version_format='{major}',
    prefix_format='/api/v{major}',
)