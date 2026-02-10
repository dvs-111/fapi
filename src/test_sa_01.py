from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker, Mapped

from sqlalchemy import create_engine

sa_engine = create_engine(
	"postgresql+psycopg://postgres:123456@localhost:5432/postgres",
	echo=True,
	)

sa_sessmaker = sessionmaker(sa_engine)

meta_obj = MetaData()

# Base = declarative_base()
class Base(DeclarativeBase):
	pass

useraccess = Table(
	"useraccess",
	meta_obj,
	Column("uid", Integer, primary_key=True),
	Column("gid", Integer, primary_key=True),
)

meta_obj.drop_all(sa_engine)
meta_obj.create_all(sa_engine)

# class User(Base):
# 	__tablename__ = "users"

# 	id = Column(Integer, primary_key=True)
# 	groups = relationship("group", secondary=useraccess, back_populates="users", cascade="all, delete-orphan")
# 	posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

# class Group(Base):
# 	__tablename__ = "groups"
# 	id = Column(Integer, primary_key=True)
# 	name = Column(String(64))

# 	users = relationship("User", secondary=useraccess, back_populates="groups")

# class Post(Base):
# 	id = Column(Integer, primary_key=True)
# 	title = Column(String(250))

from sqlalchemy import insert, select, update, text

'''
with sa_sessmaker() as conn:
	stmt = "CREATE TABLE IF NOT EXISTS aboba(a int, b int);"
	conn.execute(text(stmt))
	conn.commit()
# '''

with sa_sessmaker() as conn:
	stmt = insert(useraccess).values(
		[
			{"uid": 1, "gid": 2},
			{"uid": 3, "gid": 4}
		]
	)
	conn.execute(stmt)
	conn.commit()

with sa_sessmaker() as conn:
	stmt = select(useraccess.c.uid, useraccess.c.gid)
	x = conn.execute(stmt)
	print([i for i in x.fetchall()])