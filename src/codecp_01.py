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

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

useraccess = Table(
	"useraccess",
	meta_obj,
	Column("uid", Integer, ForeignKey("users.id"), primary_key=True),
	Column("gid", Integer, ForeignKey("groups.id"), primary_key=True)
)

meta_obj.create_all()

class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	# id = Column(Integer, primary_key=True)
	# groups: Mapped
	groups = relationship("group", secondary=useraccess, back_populates="users", cascade="all, delete-orphan")
	posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Group(Base):
	__tablename__ = "groups"
	id = Column(Integer, primary_key=True)
	name = Column(String(64))

	users = relationship("User", secondary=useraccess, back_populates="groups")

with mksess() as conn:
	conn.add(User)