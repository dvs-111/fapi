from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

sa_engine = create_engine(
	"postgresql+psycopg://postgres:123456@localhost:5432/postgres",
	echo=True,
)

mksess = sessionmaker(sa_engine)
# meta_obj = MetaData()

# ========= Модели
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Annotated, List

intpk = Annotated[int, mapped_column(primary_key=True)]
str_100 = Annotated[str, mapped_column(String(100))]

class BaseORM(DeclarativeBase):
	...
	# type_annotation_map = {
	# 	str_200: String(str_200.__metadata__[0])
	# }

class User(BaseORM):
	__tablename__ = "users"

	id: Mapped[intpk]
	name: Mapped[str_100]
	rel_msgs_sent: Mapped[List["Message"]] = relationship("Message", back_populates="sender", foreign_keys="[Message.sender]", lazy="selectin")
	rel_msgs_recv: Mapped[List["Message"]] = relationship("Message", back_populates="reciever", foreign_keys="[Message.reciever]", lazy="selectin")
	# rel_posts: Mapped[List["Post"]] = relationship(back_populates="rel_author")
	# rel_channels: Mapped[List["Channel"]] = relationship(back_populates="rel_subs")

class Message(BaseORM):
	__tablename__ = "messages"
	
	id: Mapped[intpk]
	sender: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
	reciever: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
	text: Mapped[str]
'''
class Post(BaseORM):
	__tablename__ = "posts"

	id: Mapped[intpk]
	title: Mapped[str_100]
	text: Mapped[str]
	author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"))

	# rel_author: Mapped["User"] = relationship(back_populates="rel_posts", foreign_keys=[author_id])
	# rel_channel: Mapped["User"] = relationship(back_populates="rel_posts", foreign_keys=[channel_id])

class Channel(BaseORM):
	__tablename__ = "channels"

	id: Mapped[intpk]
	name: Mapped[str]

	rel_subs: Mapped[int] = relationship(back_populates="rel_channels")

class Chunk(BaseORM):
	__tablename__ = "chunks"

	id: Mapped[intpk]
	name: Mapped[str]
# '''
# BaseORM.metadata.create_all(sa_engine)
# =========== Ручки
# === немношк пудантика шобы менять состав классов и парсить жсон

from pydantic import BaseModel as pd_Base, ConfigDict

class pd_UserPost(pd_Base):
	name: str

	model_config = ConfigDict(from_attributes=True)

class pd_MessagePost(pd_Base):
	sender: int
	reciever: int
	text: str

	model_config = ConfigDict(from_attributes=True)

class pd_ChannelPost(pd_Base):
	name: str

	model_config = ConfigDict(from_attributes=True)

class pd_PostPost(pd_Base):
	name: str

	model_config = ConfigDict(from_attributes=True)

class pd_UserOut(pd_UserPost):
	id: int

class pd_MessageOut():
	id: int
	income: bool
	text: str

class pd_PostOut(pd_PostPost):
	author: pd_UserPost          # вложенный автор (без author_id!)
	channel: pd_ChannelPost      # вложенный канал (без channel_id!)

class pd_ChannelOut(pd_ChannelPost):
	owner: pd_UserPost
	subscribers_count: int = 0          # можно считать отдельно
	posts: List[pd_PostPost] = []          # или только id постов, если много

# class pd_UserOut(pd_UserPost):
# 	owned_channels: List[pd_ChannelPost] = []
# 	subscriptions: List[pd_ChannelPost] = []

# ==== А тута прям ручки
# from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Додэп зависимостей
def get_db_dep():
	db = mksess()
	try:
		yield db
	finally:
		db.close()
get_injector = Annotated[Session, Depends(get_db_dep)]

# router = APIRouter()
app = FastAPI()

@app.post("/users/add")
def new_user(new_user: pd_UserPost, db: Session = Depends(get_db_dep)):
	print(new_user, new_user.model_dump())
	print(User.__mapper__.columns.keys())
	u = User(**new_user.model_dump())
	db.add(u)
	db.commit()
	db.refresh(u)
	return {"got": pd_UserOut(**u.__dict__)}
	# return {"got": pd_UserOut(u)}

@app.get("/users", response_model=List[pd_UserOut])
def get_user(db: Session = Depends(get_db_dep)):
	res = db.query(User).all()
	return [i for i in res]

@app.delete("/users/{uid}")
def rasstrel(uid: int, db: get_injector):
	u = db.query(User).filter(User.id == uid).delete()
	db.commit()
	return {"del"}

'''
@app.get("/messages/{sender_id}/{reciever_id}", response_model=List[pd_MessageOut])
def opn_dialog(sender_id: int, reciever_id: int, db: get_injector):
	sender = db.query(User).filter(User.id == sender_id).first()
	if not sender:
		raise HTTPException(404, "Этот гад не на парковке")
	
	reciever = db.query(User).filter(User.id == reciever_id).first()
	if not reciever:
		raise HTTPException(404, "Мысли пока не читаем. А жаль")
	
	msgs = db.query(Message).filter((Message.sender == sender_id) & (Message.reciever == reciever_id)).all()
	return [i for i in msgs]
# '''

@app.get("/messages/{sender_id}/{reciever_id}", response_model=List[pd_MessageOut])
def opn_dialog(sender_id: int, reciever_id: int, db: get_injector):
	sender = db.query(User).filter(User.id == sender_id).first()
	if not sender:
		raise HTTPException(404, "Этот гад не на парковке")
	
	reciever = db.query(User).filter(User.id == reciever_id).first()
	if not reciever:
		raise HTTPException(404, "Мысли пока не читаем. А жаль")
	
	

@app.post("/messages/send")
def send_msg(messag_new: pd_MessagePost, db: Annotated[Session, Depends(get_db_dep)]):
	sender = db.query(User).filter(User.id == messag_new.sender).first()
	if not sender:
		raise HTTPException(404, "Ты никто")
	
	reciever = db.query(User).filter(User.id == messag_new.sender).first()
	if not reciever:
		raise HTTPException(404, "Ты не путин чтобы звонить на выключенный")
	
	m = Message(**messag_new.model_dump())
	db.add(m)
	db.commit()
	db.refresh(m)
	return {"sent": pd_MessageOut(**m.__dict__)}

@app.get("/posts", response_model=pd_PostOut)
def get_posts(db: Session = Depends(get_db_dep)):
	posts = db.query(Post).all()
	if not posts:
		raise HTTPException(404, "Чота с постами")
	return posts

@app.get("/posts/{post_id}", response_model=pd_PostOut)
def get_post(post_id: int, db: Session = Depends(get_db_dep)):
	post = db.query(Post).filter(Post.id == post_id).first()
	if not post:
		raise HTTPException(404, "Пост не найден")
	return pd_PostOut.model_validate()

@app.post("/posts/post")
def new_post():
	pass
# Пуськ
if __name__ == "__main__":
	import uvicorn
	uvicorn.run(
		"test_sa_02:app",
		host="localhost",
		port=8000,
		reload=True,
	)