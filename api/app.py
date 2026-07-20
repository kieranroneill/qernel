import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api import routers
from api.dtos.system import (
    AuthConfigDTO,
    ModelConfigDTO,
    RootConfigDTO,
    SystemConfigDTO,
)
from api.utilities.database import url as database_url
from api.utilities.session import url as session_url


def _create_app() -> FastAPI:
    app_title = os.environ["APP_TITLE"]
    _app = FastAPI(lifespan=_lifespan, title=f"{app_title} API")

    # /api
    # /api/builds
    _app.include_router(routers.builds.router)
    # /health
    _app.include_router(routers.health.router)

    return _app


@asynccontextmanager
async def _lifespan(_app: FastAPI) -> AsyncIterator[None]:
    database_engine = create_async_engine(database_url(), pool_pre_ping=True)
    session_store = Redis.from_url(
        session_url(),
        encoding="utf-8",
        decode_responses=True,
    )
    workspace_root = Path("./.workspace").resolve()

    # make workspace directory if it doesn't exist
    workspace_root.mkdir(parents=True, exist_ok=True)

    # attach dependencies
    _app.state.config = SystemConfigDTO(
        auth=AuthConfigDTO(
            github_client_id=os.environ["GITHUB_CLIENT_ID"],
            github_client_secret=os.environ["GITHUB_CLIENT_SECRET"],
            github_redirect_uri=os.environ["GITHUB_REDIRECT_URI"],
            github_scope=os.environ["GITHUB_SCOPE"],
            session_cookie_name=os.environ["SESSION_COOKIE_NAME"],
            session_secret=os.environ["SESSION_SECRET"],
        ),
        model=ModelConfigDTO(
            api_key=os.environ["MODEL_API_KEY"] or None,
            base_url=os.environ["MODEL_BASE_URL"],
            model=os.environ["MODEL"],
            provider=os.environ["MODEL_PROVIDER"],
        ),
        roots=RootConfigDTO(
            project=Path(__file__).resolve().parent.parent,
            registry=Path("./registry").resolve(),
            workspace=workspace_root,
        ),
        title=_app.title,
    )
    _app.state.database = async_sessionmaker(
        bind=database_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    _app.state.session_store = session_store

    try:
        yield
    finally:
        await session_store.aclose()
        await database_engine.dispose()
    # cleanup


app = _create_app()
