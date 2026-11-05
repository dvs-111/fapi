# Сессии
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import MetaData, select
from sqlalchemy.orm import DeclarativeBase

#--------

from sqlalchemy import Table, Column, Integer, String, ForeignKey, func as sa_func, text as sa_text
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
import datetime
from typing import Annotated

sa_engine = create_engine(
	"postgresql+psycopg://postgres:123456@localhost:5432/postgres",
	echo=True,
)

mksess = sessionmaker(sa_engine)
meta_obj = MetaData()

str_200 = Annotated[str, 200]

class Base(DeclarativeBase):
	...
	# type_annotation_map = {
	# 	str_200: String(str_200.__metadata__[0])
	# }

# Зависимости всё



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

	id: Mapped[intpk]
	username: Mapped[str_200]

class Workload(enum.Enum):
	parttime = "parttime"
	fulltime = "fulltime"

class ResumeOrm(Base):
	__tablename__ = "resumes"

	id: Mapped[intpk]
	title: Mapped[str]
	zp: Mapped[int | None]
	workload: Mapped[Workload]
	worker_id: Mapped[int] = mapped_column(ForeignKey(WorkerOrm.id, ondelete="CASCADE"))
	# worker_id = Mapped[int] = mapped_column(ForeignKey(WorkerOrm.id), ondelete="SET NULL")
	# worker_id = mapped_column(ForeignKey("workers.id")) # Это шоб не надо было импорты делать
	# created_at: Mapped[datetime.datetime] = mapped_column(server_default=sa_func.now())
	created_at: Mapped[datetime.datetime] = mapped_column(server_default=sa_text("TIMEZONE('utc', now())"))
	updated_at: Mapped[datetime.datetime] = mapped_column(server_default=sa_text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.now(datetime.UTC))

Base.metadata.create_all(sa_engine)
workers = [WorkerOrm(username="Pupa"), WorkerOrm(username="Lupa")]

print(workers[0].__dict__)
from sqlalchemy import table, column
with mksess() as conn:
	# stmt = select(WorkerOrm)
	# wtab = table("workers", column("id"), column("username"))
	# stmt = select(wtab.c.id, wtab.c.username)
	# res = conn.execute(stmt)
	conn.add_all(workers)
	conn.commit()
	for w in workers:
		conn.refresh(w)
	# print([i.__dict__ for i in res.scalars().all()])
