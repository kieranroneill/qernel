from pathlib import Path

import pytest
from dotenv import load_dotenv

from api.dtos.system import RootConfigDTO


def pytest_sessionstart() -> None:
    load_dotenv(".env.test")


@pytest.fixture(scope="module")
def root_config():
    return RootConfigDTO(
        project=Path(__file__).resolve().parent,
        registry=Path("./registry").resolve(),
        workspace=Path("./.workspace").resolve(),
    )
