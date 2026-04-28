from schemas import PdBase, List
from users.schemas import PdUserPost, PdUserOut

class PdChannelPost(PdBase):
	name: str

class PdPostPost(PdBase):
	name: str

class PdPostOut(PdPostPost):
	author: PdUserPost          # вложенный автор (без author_id!)
	channel: PdChannelPost      # вложенный канал (без channel_id!)

class PdChannelOut(PdChannelPost):
	owner: PdUserPost
	subscribers_count: int = 0          # можно считать отдельно
	posts: List[PdPostPost] = []          # или только id постов, если много