from schemas import PdBase

class PdUserPost(PdBase):
	name: str

class PdUserOut(PdUserPost):
	id: int