import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv


def pytest_sessionstart() -> None:
    load_dotenv(".env.test")


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
