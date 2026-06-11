from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session

# from schemas import pd_MessagePost, pd_MessageOut, PdPostOut, pd_UserOut
from models import List, BaseORM
from users.schemas import PdUserPost, PdUserOut
from messages.schemas import PdMessagePost, PdMessageOut
from channels.schemas import PdChannelPost, PdChannelOut, PdPostPost, PdPostOut
from users.models import User
from messages.models import Message
# from channels.models import Post, Channel, Chunk
from config.db_helper import get_db, AsyncSession
from sqlalchemy import select, delete, insert, update, and_, or_
from exceptions import ExcUserExists, ExcUserNotFound

# from sqlalchemy.orm import RelationshipProperty
# for m in BaseORM.registry.mappers:
# 	for prop in m.all_orm_descriptors:
# 		if isinstance(prop, RelationshipProperty):
# 			print (f"rel-modl: {m.class_.__name__} | prop: {prop}, prop key: {prop.key}, targ {prop.argument}")
# 		else:
# 			print (f"modl: {m.class_.__name__} | prop: {prop}, prop key: {prop.key}")
BaseORM.registry.configure()

# import application
from typing import Annotated

get_injector = Annotated[AsyncSession, Depends(get_db)] # А ето видимо опять в роутыр.пу

# router = APIRouter()
router = FastAPI()

@router.post("/users/add")
async def new_user(new_user: PdPostOut, db: get_injector):
	u = User(**new_user.model_dump())
	db.add(u)
	await db.commit()
	await db.refresh(u)
	return {"got": PdUserOut(**u.__dict__)}

@router.get("/users", response_model=List[PdUserOut])
async def get_user(db: get_injector):
	res = await db.execute(select(User))
	res = res.scalars().all()
	return res

@router.delete("/users/{uid}")
async def rasstrel(uid: int, db: get_injector):
	u = await db.execute(select(User).filter(User.id == uid))
	u = u.scalar_one_or_none()
	u_ret = PdUserOut(u)
	await db.delete(u)
	await db.commit()
	return {"del"}

@router.get("/messages/{sender_id}/{receiver_id}", response_model=List[PdMessageOut])
async def opn_dialog(sender_id: int, receiver_id: int, db: get_injector):
	sender = await db.execute(select(User).filter(User.id == sender_id))
	if not sender.first():
		raise ExcUserNotFound(f"No sender: {sender_id}")
	
	receiver = await db.execute(select(User).filter(User.id == receiver_id))
	if not receiver.first():
		raise ExcUserNotFound(f"No receiver: {receiver_id}")
	
	msgs = await db.execute(select(Message).filter(and_(Message.sender == sender_id, Message.receiver == receiver_id)))
	
	m_list = msgs.scalars().all()
	print([PdMessageOut(**i.__dict__)	for i in  m_list])
	# return [PdMessageOut(**i.__dict__) for i in m_list]
	return m_list

@router.post("/messages/send")
async def send_msg(messag_new: PdMessagePost, db: get_injector):
	sender = await db.execute(select(User).filter(User.id == messag_new.sender))
	sender = sender.first()
	if not sender:
		raise ExcUserNotFound
	
	reciever = await db.execute(select(User).filter(User.id == messag_new.sender)).first()
	if not reciever:
		raise ExcUserNotFound
	
	m = Message(**messag_new.model_dump())
	db.add(m)
	await db.commit()
	await db.refresh(m)
	return {"sent": PdMessageOut(**m.__dict__)}
"""
@router.get("/posts", response_model=PdPostOut)
async def get_posts(db: get_injector):
	posts = await db.execute(select(Post)).all()
	if not posts:
		raise HTTPException(404, "Чота с постами")
	return posts

@router.get("/posts/{post_id}", response_model=PdPostOut)
async def get_post(post_id: int, db: get_injector):
	post = await db.execute(select(Post).filter(Post.id == post_id)).first()
	if not post:
		raise HTTPException(404, "Пост не найден")
	return PdPostOut.model_validate()

@router.post("/posts/post")
async def new_post():
	pass
# """