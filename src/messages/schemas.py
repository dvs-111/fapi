from schemas import PdBase

class PdMessagePost(PdBase):
	sender: int
	receiver: int
	text: str

class PdMessageOut(PdMessagePost):
	id: int
	# income: bool
	# text: str