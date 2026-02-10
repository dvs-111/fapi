# Сессии
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase



sa_engine = create_engine(
	"postgresql+psycopg://postgres:123456@localhost:5432/postgres",
	echo=True,
)

mksess = sessionmaker(sa_engine)
meta_obj = MetaData()

class Base(DeclarativeBase):
	pass

# Зависимости всё

from sqlalchemy import Table, Column, Integer, String, ForeignKey, func as sa_func, text as sa_text
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
import datetime
from typing import Annotated

# useraccess = Table(
# 	"useraccess",
# 	meta_obj,
# 	Column("uid", Integer, ForeignKey("users.id"), primary_key=True),
# 	Column("gid", Integer, ForeignKey("groups.id"), primary_key=True)
# )

# meta_obj.create_all()

intpk = Annotated[int, mapped_column(primary_key=True)]

class WorkerOrm(Base):
	__tablename__ = "workers"

	id: Mapped[int] = mapped_column(primary_key=True)
	username: Mapped[str]

class Workload(enum.Enum):
	parttime = "parttime"
	fulltime = "fulltime"

class ResumeOrm(Base):
	__tablename__ = "resumes"

	id: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str]
	zp: Mapped[int | None]
	workload: Mapped[Workload]
	worker_id = Mapped[int] = mapped_column(ForeignKey(WorkerOrm.id), ondelete="CASCADE")
	# worker_id = Mapped[int] = mapped_column(ForeignKey(WorkerOrm.id), ondelete="SET NULL")
	# worker_id = mapped_column(ForeignKey("workers.id")) # Это шоб не надо было импорты делать
	# created_at: Mapped[datetime.datetime] = mapped_column(server_default=sa_func.now())
	created_at: Mapped[datetime.datetime] = mapped_column(server_default=sa_text("TIMEZONE('utc', now())"))
	updated_at: Mapped[datetime.datetime] = mapped_column(server_default=sa_text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.now(datetime.UTC))