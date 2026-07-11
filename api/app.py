import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from api import routers
from api.dtos.system import ModelConfigDTO, RootConfigDTO, SystemConfigDTO


def _app() -> FastAPI:
    app_title = os.environ["APP_TITLE"]
    __app = FastAPI(lifespan=_lifespan, title=f"{app_title} API")

    __app.include_router(routers.builds.router)
    __app.include_router(routers.health.router)

    return __app


@asynccontextmanager
async def _lifespan(__app: FastAPI) -> AsyncIterator[None]:
    workspace_root = Path("./.workspace").resolve()

    workspace_root.mkdir(parents=True, exist_ok=True)

    # attach dependencies
    __app.state.config = SystemConfigDTO(
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
        title=__app.title,
    )

    yield
    # cleanup


app = _app()
