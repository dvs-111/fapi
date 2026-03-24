from src.schemas import *
from src.users.schemas import *

class pd_ChannelPost(pd_Base):
	name: str

class pd_PostPost(pd_Base):
	name: str

class pd_PostOut(pd_PostPost):
	author: pd_UserPost          # вложенный автор (без author_id!)
	channel: pd_ChannelPost      # вложенный канал (без channel_id!)

class pd_ChannelOut(pd_ChannelPost):
	owner: pd_UserPost
	subscribers_count: int = 0          # можно считать отдельно
	posts: List[pd_PostPost] = []          # или только id постов, если много