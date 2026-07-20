from abc import ABC, abstractmethod
from logging import Logger
from typing import Generic, TypeVar

from redis.asyncio import Redis

from api.utilities.logging import get_logger

DTO = TypeVar("DTO")


class BaseSessionRepository(ABC, Generic[DTO]):
    def __init__(self, session_store: Redis, logger: Logger | None = None) -> None:
        self._logger = logger or get_logger()
        self._session_store = session_store

    ##
    # private methods
    ##
    @abstractmethod
    def _key(self, _id: str) -> str:
        raise NotImplementedError

    ##
    # public methods
    ##
    @abstractmethod
    async def add(self, dto: DTO) -> DTO:
        raise NotImplementedError

    async def delete_by_id(self, _id: str) -> bool:
        await self._session_store.delete(self._key(_id))

        self._logger.debug('deleted "%s"', self._key(_id))

        return True

    @abstractmethod
    async def get_by_id(self, _id: str) -> DTO | None:
        raise NotImplementedError
