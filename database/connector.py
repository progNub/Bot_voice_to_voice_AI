from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool


class AsyncConnection:

    def __init__(self):
        self._engine = None
        self._session = None

    def initialize(self, dsn: str, echo=True):
        """Example: 'sqlite+aiosqlite:///db.sqlite3'"""
        self._engine = create_async_engine(dsn, echo=echo, poolclass=AsyncAdaptedQueuePool)
        self._session = AsyncSession(self._engine)

    @property
    def session(self) -> AsyncSession:
        return self._session

    @property
    def engine(self) -> AsyncEngine:
        return self._engine


db_conn = AsyncConnection()
