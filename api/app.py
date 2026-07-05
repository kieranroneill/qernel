import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import routers


def _app() -> FastAPI:
    app_title = os.environ["APP_TITLE"]
    __app = FastAPI(lifespan=_lifespan, title=f"{app_title} API")

    __app.include_router(routers.health.router)

    return __app


@asynccontextmanager
async def _lifespan(__app: FastAPI) -> AsyncIterator[None]:
    # attach dependencies

    yield
    # cleanup


app = _app()
