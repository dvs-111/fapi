from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# from schemas import pd_MessagePost, pd_MessageOut, pd_UserPost, pd_UserOut
from users.schemas import *
from messages.schemas import *
from channels.schemas import *
from users.models import *
from messages.models import *
from channels.models import *
from config.db_helper import *
import application

from typing import Annotated

get_injector = Annotated[Session, Depends(mksess)] # А ето видимо опять в роутыр.пу

# router = APIRouter()
app = FastAPI()
# app = application.get_app()

@app.post("/users/add")
def new_user(new_user: pd_UserPost, db: get_injector):
	print(new_user, new_user.model_dump())
	print(User.__mapper__.columns.keys())
	u = User(**new_user.model_dump())
	db.add(u)
	db.commit()
	db.refresh(u)
	return {"got": pd_UserOut(**u.__dict__)}
	# return {"got": pd_UserOut(u)}

@app.get("/users", response_model=List[pd_UserOut])
def get_user(db: get_injector):
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
def send_msg(messag_new: pd_MessagePost, db: get_injector):
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
def get_posts(db: get_injector):
	posts = db.query(Post).all()
	if not posts:
		raise HTTPException(404, "Чота с постами")
	return posts

@app.get("/posts/{post_id}", response_model=pd_PostOut)
def get_post(post_id: int, db: get_injector):
	post = db.query(Post).filter(Post.id == post_id).first()
	if not post:
		raise HTTPException(404, "Пост не найден")
	return pd_PostOut.model_validate()

@app.post("/posts/post")
def new_post():
	pass