from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import Settings

from typing import Annotated

settings = Settings()

engine = create_engine(str(settings.postgres_url))
# sa_engine = create_engine(
# 	"postgresql+psycopg://postgres:123456@localhost:5432/postgres",
# 	echo=True,
# )
# sess_mkr = sessionmaker(sa_engine)

@contextmanager
async def mksess() -> Session:
	session: Session = Session(engine)
	try:
		yield session
		session.commit()
	except Exception:
		session.rollback()
		raise
	finally:
		session.close()

# get_injector = Annotated[Session, Depends(mksess)]