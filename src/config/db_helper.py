from contextlib import asynccontextmanager

# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import Session

from config.db_config import Settings

from typing import Annotated

settings = Settings()

engine = create_async_engine(str(settings.postgres_url))
# sa_engine = create_engine(
# 	"postgresql+psycopg://postgres:123456@localhost:5432/postgres",
# 	echo=True,
# )
# sess_mkr = sessionmaker(sa_engine)

@asynccontextmanager
async def get_session():
	session: AsyncSession = AsyncSession(engine)
	try:
		yield session
		await session.commit()
	except Exception:
		await session.rollback()
		raise
	finally:
		await session.close()

async def get_db() -> AsyncSession:
	async with get_session() as sess:
		yield sess
# get_injector = Annotated[Session, Depends(mksess)]