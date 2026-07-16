from schemas import PdBase, List
from users.schemas import PdUserPost, PdUserOut

class PdChannelPost(PdBase):
	name: str
	owner: int

class PdChannelOut(PdChannelPost):
	id: int

class PdPostPost(PdBase):
	name: str
	author: int
	channel: int

class PdPostOut(PdPostPost):
	id: int

class PdChunkPost(PdBase):
	name: str

class PdChunkOut(PdChannelPost):
	id: int