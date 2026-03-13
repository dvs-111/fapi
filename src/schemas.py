
from pydantic import BaseModel as pd_BaseModel, ConfigDict
from typing import List

class pd_Base(pd_BaseModel):
	model_config = ConfigDict(from_attributes=True)

class pd_UserPost(pd_Base):
	name: str

class pd_MessagePost(pd_Base):
	sender: int
	reciever: int
	text: str

class pd_ChannelPost(pd_Base):
	name: str

class pd_PostPost(pd_Base):
	name: str

class pd_UserOut(pd_UserPost):
	id: int

class pd_MessageOut(pd_Base):
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