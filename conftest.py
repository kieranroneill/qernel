from pathlib import Path

import pytest

from api.dtos.system import RootConfigDTO


@pytest.fixture(scope="module")
def root_config():
    return RootConfigDTO(
        project=Path(__file__).resolve().parent,
        registry=Path("./registry").resolve(),
        workspace=Path("./.workspace").resolve(),
    )
